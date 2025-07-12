import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def transcribe_audio(filepath: str) -> str:
    try:
        print(f"🔍 Groq Whisper v3: Transcribing {filepath}")
        with open(filepath, "rb") as f:
            response = client.audio.transcriptions.create(
                file=f,
                model="whisper-large-v3"
            )
        return response.text
    except Exception as e:
        print("❌ Transcription failed:", e)
        return ""