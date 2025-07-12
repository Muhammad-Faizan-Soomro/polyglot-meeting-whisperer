import sounddevice as sd
import numpy as np
from transcribe import transcribe_audio
import threading
import time

SAMPLE_RATE = 22050
CHANNELS = 1
CHUNK_DURATION = 5  # seconds
CHUNK_SIZE = SAMPLE_RATE * CHUNK_DURATION

def get_device_index(name_contains: str, is_input=True, limit=10):
    devices = sd.query_devices()[:limit]  # only consider top N devices
    for i, device in enumerate(devices):
        if name_contains.lower() in device['name'].lower() and (
            (is_input and device['max_input_channels'] > 0) or
            (not is_input and device['max_output_channels'] > 0)
        ):
            print(f"✅ Found '{name_contains}' as device index: {i}")
            return i
    print(f"⚠️ Could not find device with name containing: {name_contains} in top {limit} devices.")
    return None

# Try detecting devices
MIC_DEVICE_INDEX = get_device_index("microphone", is_input=True)
LOOPBACK_DEVICE_INDEX = get_device_index("stereo mix", is_input=True)

# Control flags
recording = False
mic_stream = None
loopback_stream = None

# Shared chunk buffers
mic_chunks = []
loopback_chunks = []

def mic_callback(indata, frames, time_info, status):
    if status:
        print("⚠️ Mic:", status)
    mic_chunks.append(indata.copy())

def loopback_callback(indata, frames, time_info, status):
    if status:
        print("⚠️ Loopback:", status)
    loopback_chunks.append(indata.copy())

def chunk_processor():
    while recording:
        if LOOPBACK_DEVICE_INDEX is not None:
            if len(mic_chunks) > 0 and len(loopback_chunks) > 0:
                mic_chunk = mic_chunks.pop(0)
                loopback_chunk = loopback_chunks.pop(0)
                combined = ((mic_chunk.astype(np.int32) + loopback_chunk.astype(np.int32)) // 2).astype(np.int16)
                audio_bytes = combined.tobytes()
            else:
                time.sleep(0.1)
                continue
        else:
            if len(mic_chunks) > 0:
                mic_chunk = mic_chunks.pop(0)
                audio_bytes = mic_chunk.astype(np.int16).tobytes()
            else:
                time.sleep(0.1)
                continue

        transcript = transcribe_audio(audio_bytes)
        if transcript.strip():
            print("📝 Transcript added.")
            with open("transcripts.txt", "a", encoding="utf-8") as f:
                f.write(transcript.strip() + "\n")
        else:
            print("🌀 No speech detected.")

def record_loop():
    global mic_stream, loopback_stream, recording

    if MIC_DEVICE_INDEX is None:
        print("❌ No microphone device found. Aborting.")
        return

    try:
        print("🔊 Starting recording...")

        mic_stream = sd.InputStream(
            device=MIC_DEVICE_INDEX,
            channels=CHANNELS,
            samplerate=SAMPLE_RATE,
            dtype='int16',
            callback=mic_callback,
            blocksize=CHUNK_SIZE
        )

        if LOOPBACK_DEVICE_INDEX is not None:
            loopback_stream = sd.InputStream(
                device=LOOPBACK_DEVICE_INDEX,
                channels=CHANNELS,
                samplerate=SAMPLE_RATE,
                dtype='int16',
                callback=loopback_callback,
                blocksize=CHUNK_SIZE
            )

        mic_stream.start()
        print("🎤 Mic stream started.")

        if LOOPBACK_DEVICE_INDEX is not None:
            loopback_stream.start()
            print("🔁 Loopback stream started.")
        else:
            print("⚠️ Loopback device not found. Running in mic-only mode.")

        threading.Thread(target=chunk_processor, daemon=True).start()

        while recording:
            time.sleep(0.1)

        print("🛑 Stopping streams...")
        mic_stream.stop(); mic_stream.close()
        if loopback_stream:
            loopback_stream.stop(); loopback_stream.close()

    except Exception as e:
        print("❌ Error during stream startup:", e)

def start_loopback():
    global recording
    if not recording:
        recording = True
        threading.Thread(target=record_loop, daemon=True).start()

def stop_loopback():
    global recording
    recording = False

