# agents/transcribe_agent.py

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class TranscribeAgent:
    def __init__(self, model_name="whisper-large-v3"):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment.")
        self.client = Groq(api_key=self.api_key)
        self.model_name = model_name

    def run(self, audio_file_path: str) -> str:
        """
        Transcribe the given audio file using Groq Whisper.
        Returns the transcribed text, or an empty string on failure.
        """
        try:
            print(f"🔍 TranscribeAgent: Transcribing {audio_file_path}")
            with open(audio_file_path, "rb") as audio_file:
                response = self.client.audio.transcriptions.create(
                    file=audio_file,
                    model=self.model_name
                )
            transcript = response.text.strip()
            if transcript:
                print(f"📝 Transcript: {transcript}")
            else:
                print("🌀 No speech detected.")
            return transcript
        except Exception as e:
            print("❌ Transcription failed:", e)
            return ""