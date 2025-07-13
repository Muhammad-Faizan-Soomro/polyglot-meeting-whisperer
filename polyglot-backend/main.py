# filename: main.py (The RE-WIRED version)

import asyncio
import json
import base64
import numpy as np
import time
import os
import io
from typing import Dict, List, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
import openai
from pydub import AudioSegment
from dotenv import load_dotenv
import websockets 


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


app = FastAPI()


GENAIOS_WS_URL = os.getenv("GENAIOS_WEBSOCKET_URL", "ws://localhost:8080/ws/chat")


class PolyglotWhispererClient:
    """
    This class now acts as a CLIENT to the GenAIOS ecosystem.
    It handles the UI-facing WebSocket, performs the initial transcription,
    and then delegates the complex work (Translate, Summarize) to the GenAIOS Master Agent.
    """
    
    def __init__(self):

        self.selected_languages = ["Chinese", "French"]


    def _convert_to_wav(self, audio_np: np.ndarray, sample_rate: int) -> bytes:
        """Converts a numpy array of audio data to WAV format bytes."""
        try:
            wav_io = io.BytesIO()
            audio_segment = AudioSegment(
                audio_np.tobytes(),
                frame_rate=sample_rate,
                sample_width=audio_np.dtype.itemsize,
                channels=1
            )
            audio_segment.export(wav_io, format="wav")
            wav_io.seek(0)
            return wav_io.read()
        except Exception as e:
            raise Exception(f"Error converting numpy audio to WAV: {str(e)}")

    async def _transcribe_audio_with_whisper(self, audio_data_hex: str, sample_rate: int) -> Dict[str, Any]:
        """Transcribes audio using OpenAI's Whisper API."""
        try:
            audio_bytes = bytes.fromhex(audio_data_hex)
            audio_np = np.frombuffer(audio_bytes, dtype=np.float32)
            wav_bytes = self._convert_to_wav(audio_np, sample_rate)
            
            audio_file = io.BytesIO(wav_bytes)
            audio_file.name = "input_audio.wav"
            
            client = openai.AsyncOpenAI()
            transcript_response = await client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            
            return {"success": True, "text": transcript_response.text}
        except Exception as e:
            print(f"Error during Whisper transcription: {str(e)}")
            return {"success": False, "error": str(e)}

    
    async def orchestrate_with_genaios(self, original_text: str, languages: List[str]) -> Dict[str, Any]:
        """
        Connects to the GenAIOS Master Agent and sends a complex task request.
        """
        print(f"Connecting to GenAIOS at {GENAIOS_WS_URL} to orchestrate task...")

        prompt_for_master_agent = f"""
        A user has provided the following text from a meeting: "{original_text}"

        Please orchestrate a workflow to achieve the following goals:
        1. First, use the 'summarizer_agent' to create a concise summary of the text.
        2. Second, use the 'translator_agent' to translate ONLY the generated summary into the following languages: {json.dumps(languages)}.
        3. Third, use the 'questions_agent' to generate follow-up questions based on the original text.

        After all steps are complete, please return a single, final JSON object with three keys: 'summary', 'translations', and 'questions'.
        """
        
        try:
            async with websockets.connect(GENAIOS_WS_URL) as genaios_socket:
                
                await genaios_socket.send(json.dumps({
                    "type": "chat_message", 
                    "content": prompt_for_master_agent
                }))
                
                
                print("Task sent to GenAIOS. Awaiting final result...")
                response_str = await genaios_socket.recv()
                print(f"Received final result from GenAIOS: {response_str}")
                
                
                try:
                
                    response_data = json.loads(response_str)
                
                    final_payload = json.loads(response_data.get('content', '{}'))
                    return {"success": True, "data": final_payload}
                except json.JSONDecodeError:
                
                    return {"success": True, "data": {"raw_response": response_str}}

        except Exception as e:
            error_message = f"Failed to connect or communicate with GenAIOS: {str(e)}"
            print(error_message)
            return {"success": False, "error": error_message}


    
    async def handle_connection(self, websocket: WebSocket):
        """Handle incoming WebSocket connections from the Gradio frontend."""
        await websocket.accept()
        print(f"Gradio frontend client connected.")
        
        try:
            while True:
                message_str = await websocket.receive_text()
                data = json.loads(message_str)
                message_type = data.get("type")
                
                if message_type == "set_languages":
                    self.selected_languages = data.get("languages", ["Chinese", "French"])
                    print(f"Updated languages to: {self.selected_languages}")
                    await websocket.send_text(json.dumps({"type": "status", "message": "Languages updated."}))

                elif message_type == "process_audio":
                    await websocket.send_text(json.dumps({"type": "status", "message": "Received audio. Transcribing..."}))
                    
    
                    transcription = await self._transcribe_audio_with_whisper(
                        data.get("audio_data"),
                        data.get("sample_rate")
                    )
                    
                    if not transcription["success"]:
                        await websocket.send_text(json.dumps({"type": "error", "message": transcription["error"]}))
                        continue
                    
                    original_text = transcription["text"]
                    await websocket.send_text(json.dumps({"type": "transcript", "text": original_text}))
                    await websocket.send_text(json.dumps({"type": "status", "message": "Transcription complete. Orchestrating with GenAIOS..."}))

                    
                    final_result = await self.orchestrate_with_genaios(original_text, self.selected_languages)

                    if final_result["success"]:
                        await websocket.send_text(json.dumps({"type": "final_result", "data": final_result["data"]}))
                        await websocket.send_text(json.dumps({"type": "status", "message": "Done."}))
                    else:
                        await websocket.send_text(json.dumps({"type": "error", "message": final_result["error"]}))
                
        except WebSocketDisconnect:
            print("Gradio frontend client disconnected.")
        except Exception as e:
            print(f"An error occurred in the main WebSocket handler: {str(e)}")



client_agent = PolyglotWhispererClient()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await client_agent.handle_connection(websocket)


if __name__ == "__main__":
    print("Starting Polyglot Whisperer Client Backend...")
    uvicorn.run(app, host="0.0.0.0", port=8008)