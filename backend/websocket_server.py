import asyncio
import websockets
import tempfile
import os
import json

from agents.transcribe_agent import TranscribeAgent
from agents.translate_agent import TranslateAgent 
from agents.summarizer_agent import SummarizerAgent
from agents.question_generator_agent import QuestionGeneratorAgent
from agents.keyword_explainer_agent import KeywordExplainerAgent

PORT = 8765

# Agents
transcribe_agent = TranscribeAgent()
translate_agent = TranslateAgent()
summarizer_agent = SummarizerAgent()
question_generator_agent = QuestionGeneratorAgent()
keyword_agent = KeywordExplainerAgent()

# Shared Queue for processing audio
QUEUE = asyncio.Queue()

# Map websocket -> language preference
client_lang_map = {}

# Async worker that handles queued audio
async def transcribe_worker():
    while True:
        item = await QUEUE.get()
        file_path, websocket = item["file_path"], item["websocket"]
        target_lang = client_lang_map.get(websocket, "en")  # default fallback

        try:
            transcript = transcribe_agent.run(file_path)

            if transcript:
                await websocket.send(json.dumps({
                    "type": "transcript",
                    "data": transcript
                }))

                translated = translate_agent.run(transcript, target_language=target_lang)
                await websocket.send(json.dumps({
                    "type": "translated",
                    "data": translated
                }))

                explanations = keyword_agent.run(transcript)
                await websocket.send(json.dumps({
                    "type": "keywords",
                    "data": explanations
                }))

                summary = summarizer_agent.add_chunk(transcript, target_language=target_lang)
                if summary:
                    await websocket.send(json.dumps({
                        "type": "summary",
                        "data": summary
                    }))

                    questions = question_generator_agent.run(summary, target_language=target_lang)

                    if questions:
                        await websocket.send(json.dumps({
                            "type": "questions",
                            "data": questions
                        }))
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

# Main handler per websocket client
async def handle_connection(websocket):
    print("✅ Client connected.")
    client_lang_map[websocket] = "en"  # Default to English

    try:
        while True:
            message = await websocket.recv()

            if isinstance(message, bytes):
                print("📦 Received audio chunk.")
                try:
                    with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp_file:
                        tmp_file.write(message)
                        tmp_path = tmp_file.name

                    await QUEUE.put({ "file_path": tmp_path, "websocket": websocket })

                except Exception as e:
                    print("❌ Error handling incoming chunk:", e)

            elif isinstance(message, str):
                try:
                    data = json.loads(message)
                    if data.get("type") == "config":
                        language = data.get("language", "en")
                        client_lang_map[websocket] = language
                        print(f"🌐 Language set to: {language}")
                    else:
                        print("⚠️ Unknown message type.")
                except Exception as e:
                    print("⚠️ Failed to parse JSON config:", e)
            else:
                print("⚠️ Unknown message format. Ignored.")

    except websockets.exceptions.ConnectionClosed as e:
        print(f"❌ WebSocket closed. Code: {e.code}, Reason: {e.reason}")
    except Exception as e:
        print("❌ Unexpected error in handler:", e)
    finally:
        client_lang_map.pop(websocket, None)

# Server entrypoint
async def main():
    print(f"🌐 WebSocket server running on ws://localhost:{PORT}")
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
