import asyncio
import websockets
import tempfile
import os
from transcribe import transcribe_audio

PORT = 8765

async def handle_connection(websocket):
    print("✅ Client connected.")
    try:
        while True:
            try:
                message = await websocket.recv()

                if isinstance(message, bytes):
                    print("📦 Received audio chunk.")
                    tmp_webm_path = None

                    try:
                        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp_file:
                            tmp_file.write(message)
                            tmp_webm_path = tmp_file.name

                        transcript = transcribe_audio(tmp_webm_path)
                        if transcript.strip():
                            print("📝 Transcript:", transcript.strip())
                            with open("transcripts.txt", "a", encoding="utf-8") as f:
                                f.write(transcript.strip() + "\n")
                        else:
                            print("🌀 No speech detected.")

                    except Exception as e:
                        print("❌ Error during transcription:", e)

                    finally:
                        if tmp_webm_path and os.path.exists(tmp_webm_path):
                            try:
                                os.remove(tmp_webm_path)
                            except Exception as e:
                                print("⚠️ Could not delete temp file:", e)

                else:
                    print("⚠️ Received non-binary message. Ignoring.")

            except websockets.exceptions.ConnectionClosed as e:
                print(f"❌ WebSocket closed. Code: {e.code}, Reason: {e.reason}")
                break
            except Exception as e:
                print("⚠️ Error inside message handler:", e)

    except Exception as e:
        print("❌ Unexpected error in handler:", e)

async def main():
    print(f"🌐 WebSocket server running on ws://localhost:{PORT}")
    async with websockets.serve(
        handle_connection,
        "localhost",
        PORT,
        max_size=10_000_000,
        ping_interval=None
    ):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())