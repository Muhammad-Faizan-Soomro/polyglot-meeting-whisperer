import os
import gradio as gr
import numpy as np
import websocket
import json
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# WebSocket connection URL - configurable
WEBSOCKET_URL = os.getenv("WEBSOCKET_URL", "ws://localhost:8008/ws")

def process_audio(audio):
    """Process audio data and send to backend"""
    if audio is None:
        return "No audio detected", "", "", ""
    
    try:
        # Extract audio data
        sample_rate, audio_np = audio
        
        # Log the audio data for debugging
        print(f"Received audio: sample_rate={sample_rate}, shape={audio_np.shape}")
        
        # Simulate processing - in a real implementation, this would send to backend
        # We're avoiding WebSocket for now to isolate the recording stop issue
        time.sleep(1)  # Simulate processing time
        
        return "Audio processed successfully", "Transcript placeholder", "Translations placeholder", "Summary placeholder"
        
    except Exception as e:
        print(f"Error processing audio: {str(e)}")
        return f"Error: {str(e)}", "", "", ""

def simple_interface():
    """Create a very simple interface with minimal functionality"""
    with gr.Blocks() as interface:
        gr.Markdown("# Polyglot Meeting Whisperer")
        gr.Markdown("Record audio to test the interface.")
        
        audio_input = gr.Audio(sources=["microphone"], type="numpy", label="Record Audio")
        status = gr.Textbox(label="Status", value="Ready to record")
        transcript = gr.Textbox(label="Original Transcript", value="")
        translations = gr.Textbox(label="Translations", value="")
        summary = gr.Textbox(label="Summary", value="")
        
        # Handle audio submission
        audio_input.change(
            fn=process_audio,
            inputs=[audio_input],
            outputs=[status, transcript, translations, summary]
        )
    
    return interface

if __name__ == "__main__":
    app = simple_interface()
    app.launch(server_name="0.0.0.0", server_port=7860, share=False)
