# filename: app.py (The FINAL, working version)

import os
import gradio as gr
import numpy as np
import json
from dotenv import load_dotenv
import websockets  
import asyncio      


load_dotenv()
WEBSOCKET_URL = os.getenv("BACKEND_WEBSOCKET_URL", "ws://localhost:8008/ws")


async def run_full_process(audio):
    """
    This function now connects to our FastAPI backend (main.py) via WebSocket,
    sends the audio, and waits for the final results.
    """
    if audio is None:
        return "Please record audio first.", "", "", ""    
    try:
        sample_rate, audio_np = audio
        print(f"Gradio: Received audio, preparing to send to backend at {WEBSOCKET_URL}")

        audio_hex = audio_np.astype(np.float32).tobytes().hex()

        message_to_send = json.dumps({
            "type": "process_audio",
            "audio_data": audio_hex,
            "sample_rate": sample_rate,
            "languages": ["Chinese", "French", "Arabic"] 
        })

        async with websockets.connect(WEBSOCKET_URL) as websocket:
            print("Gradio: Connected to backend. Sending audio data...")
            await websocket.send(message_to_send)
            
            status = "Sent. Waiting for response..."
            transcript = "Processing..."
            translations = "Processing..."
            summary = "Processing..."

            while True:
                try:
                    response_str = await asyncio.wait_for(websocket.recv(), timeout=60.0)
                    response = json.loads(response_str)
                    response_type = response.get("type")                    
                    print(f"Gradio: Received message from backend -> Type: {response_type}")
                    if response_type == "status":
                        status = response.get("message", status)
                    elif response_type == "transcript":
                        transcript = response.get("text", transcript)
                    elif response_type == "final_result":
                        final_data = response.get("data", {})
                        summary = final_data.get("summary", "No summary found.")
                        translations_obj = final_data.get("translations", {})
                        translations = "\n".join([f"{lang}: {text}" for lang, text in translations_obj.items()])
                        # questions = final_data.get("questions", "No questions found.")
                        
                        status = "Done! All results received."
                        break
                    elif response_type == "error":
                        status = f"Error: {response.get('message')}"
                        break 

                except asyncio.TimeoutError:
                    status = "Connection timed out. Did the backend process take too long?"
                    break
                except websockets.exceptions.ConnectionClosed:
                    status = "Connection with backend was closed."
                    break
            
            return status, transcript, translations, summary

    except Exception as e:
        error_message = f"Critical error in Gradio interface: {str(e)}"
        print(error_message)
        return error_message, "", "", ""


def simple_interface():
    with gr.Blocks(title="Polyglot Meeting Whisperer") as interface:
        gr.Markdown("# Polyglot Meeting Whisperer")
        gr.Markdown("Record your meeting snippet, and let the agent orchestra do the work!")
        
        with gr.Row():
            audio_input = gr.Audio(sources=["microphone"], type="numpy", label="Record Audio Here")
        
        with gr.Row():
            status = gr.Textbox(label="Status", value="Ready to record...", interactive=False)
        
        with gr.Row():
            transcript = gr.Textbox(label="Original Transcript", lines=5, interactive=False)
        
        with gr.Row():
            translations = gr.Textbox(label="Summary Translations", lines=5, interactive=False)
            summary = gr.Textbox(label="Key-Point Summary", lines=5, interactive=False)
        
        audio_input.stop_recording(
            fn=run_full_process, 
            inputs=[audio_input],
            outputs=[status, transcript, translations, summary]
        )
    
    return interface


if __name__ == "__main__":
    # pip install websockets
    app = simple_interface()
    # share=True 
    app.launch(server_name="0.0.0.0", server_port=7860, share=True)