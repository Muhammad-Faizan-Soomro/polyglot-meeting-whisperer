import os
import tempfile
import wave
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def transcribe_audio(audio_bytes: bytes, sample_rate=16000) -> str:
    # Save audio to temp .wav file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        with wave.open(tmp_file, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(audio_bytes)
        tmp_path = tmp_file.name

    try:
        print(f"🔍 Groq Whisper v3: Transcribing {tmp_path}")
        with open(tmp_path, "rb") as f:
            response = client.audio.transcriptions.create(
                file=f,
                model="whisper-large-v3"
            )
        return response.text
    except Exception as e:
        print("❌ Groq Whisper failed:", e)
        return ""
    finally:
        os.remove(tmp_path)
