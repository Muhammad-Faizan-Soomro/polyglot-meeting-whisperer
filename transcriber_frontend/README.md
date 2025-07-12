# 🧠 Polyglot Meeting Whisperer (Transcription Core)

This project captures **microphone audio** directly from the **browser**, streams it to a **Python WebSocket server**, and transcribes it using **Groq Whisper v3 Large model**. Results are saved live to `transcripts.txt`.

🎛️ Controlled entirely from the browser via `index.html`.

---

## ✅ What This Project Does

- 🎤 Captures microphone input from the browser
- 📤 Sends 5-second audio chunks to backend via WebSocket
- 🧠 Transcribes each chunk using **Groq Whisper v3**
- 📝 Appends each transcript to `transcripts.txt`
- 🌐 Controlled via Start/Stop buttons in `index.html`

---

## ⚙️ Setup Instructions

### 1. Install Requirements

```bash
pip install -r requirements.txt
```
    ✅ Python 3.9+ recommended.

### 2. Set Your Groq API Key

Create a .env file in the root directory with:

GROQ_API_KEY=your_groq_api_key_here

### 🚀 How to Run
1. Start the Backend WebSocket Server

python transcriber_frontend/websocket_server.py

    WebSocket will start at: ws://localhost:8765

2. Serve the Frontend via HTTP

Don't open the HTML file directly — serve it using an HTTP server:

cd transcriber_frontend

python -m http.server 5500

Then open: http://localhost:5500

    This avoids browser auto-disconnect issues with WebSocket.

🧩 Output

    🗂️ All transcripts saved in real time to: transcripts.txt

    ✅ Each 5-second chunk is independently transcribed and logged

📎 Key Files

    transcriber_frontend/websocket_server.py – WebSocket backend to receive audio and transcribe

    transcriber_frontend/transcribe.py – Sends received .webm chunks to Groq API

    transcriber_frontend/index.html – Browser interface with Start/Stop buttons

    transcripts.txt – Transcript output (auto-created)

    .env – Holds your GROQ_API_KEY

    requirements.txt – Python dependencies

🧠 How It Works

    Frontend captures mic in 5s chunks and sends full .webm files

    Backend receives each chunk and sends directly to Groq (no FFmpeg)

    No system audio or third-party tools like VB-Cable required

🎧 Just run the backend, start the HTTP server, open the browser — and watch live transcription!
