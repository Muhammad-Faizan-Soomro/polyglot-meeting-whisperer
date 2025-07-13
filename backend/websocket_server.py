import asyncio
import websockets
import tempfile
import os

from agents.transcribe_agent import TranscribeAgent
from agents.translate_agent import TranslateAgent 
from agents.summarizer_agent import SummarizerAgent
from agents.question_generator_agent import QuestionGeneratorAgent

PORT = 8765
QUEUE = asyncio.Queue()

# Instantiate agents
transcribe_agent = TranscribeAgent()
translate_agent = TranslateAgent()
summarizer_agent = SummarizerAgent()
question_generator_agent = QuestionGeneratorAgent()

async def transcribe_worker():
    while True:
        file_path = await QUEUE.get()
        try:
            transcript = transcribe_agent.run(file_path)
            if transcript:
                # print("📝 Transcript:", transcript)

                # Translate the transcript
                translated = translate_agent.run(transcript, target_language="Spanish")
                # print("🌍 Translated:", translated)

                # Save both to file
                with open("transcripts.txt", "a", encoding="utf-8") as f:
                    f.write("Transcript: " + transcript + "\n")
                    f.write("Translation: " + translated + "\n\n")

                
                # Add to summary agent
                summary = summarizer_agent.add_chunk(transcript, target_language="Roman Urdu")
                if summary:
                    print("📚 Summary updated.")

                    questions = question_generator_agent.run(summary)
                    if questions:
                        with open("questions.txt", "a", encoding="utf-8") as qf:
                            qf.write("From Summary:\n" + summary + "\n")
                            for q in questions:
                                qf.write("Q: " + q + "\n")
                            qf.write("\n")
                        print("❓ Questions saved.")
                    else:
                        print("⚠️ No questions generated.")

            else:
                print("🌀 No speech detected.")
        except Exception as e:
            print("❌ Error in transcription pipeline:", e)
        finally:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    print("⚠️ Could not delete temp file:", e)
            QUEUE.task_done()

async def handle_connection(websocket):
    print("✅ Client connected.")
    try:
        while True:
            try:
                message = await websocket.recv()

                if isinstance(message, bytes):
                    print("📦 Received audio chunk.")
                    try:
                        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp_file:
                            tmp_file.write(message)
                            tmp_path = tmp_file.name

                        # Enqueue the file path for processing
                        await QUEUE.put(tmp_path)

                    except Exception as e:
                        print("❌ Error handling incoming chunk:", e)
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
    # Start transcriber worker in background
    asyncio.create_task(transcribe_worker())

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
