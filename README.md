# 🧠 Polyglot Meeting Whisperer (Transcription Core)

This project captures **system + microphone audio** in real time, transcribes it using **Groq Whisper v3 Large model**, and stores results in `transcripts.txt`.

🎛️ Controlled from the browser via a WebSocket-connected `test/index.html` file.

---

## ✅ What This Code Does

- 🔊 Captures mic and system audio (5-second chunks)
- 🧠 Transcribes using **Groq Whisper Large v3**
- 📝 Appends transcript to `transcripts.txt` on each chunk
- 🌐 Web-controlled using buttons in `index.html`

---

## ⚙️ Setup Instructions

### 1. Install Requirements

```bash
pip install -r requirements.txt

    Python 3.9+ is recommended.

2. Create .env File

Create a .env file in the root directory:

GROQ_API_KEY=your_groq_api_key_here

3. Enable 'Stereo Mix' (Windows only)

To allow system audio recording:

    Open Sound Settings → Recording Tab

    Right-click → Enable Stereo Mix

    If unavailable, app falls back to mic-only mode

🚀 Running the App
1. Start Backend WebSocket Server

python transcriber/websocket_server.py

Starts at: ws://localhost:8765
2. Open the Controller Web Page

Double-click or open test/index.html in a browser (Chrome/Edge/Firefox).

This page includes:

    ▶️ Start Recording – sends start-recording to backend

    ⏹ Stop Recording – sends stop-recording to backend

📁 Output

Transcripts are saved in real time to:

transcripts.txt

Each 5-second chunk is transcribed and logged immediately.
🛠 Notes

    Automatically detects mic and system devices (top 10).

    Uses Groq API — very fast + no GPU required locally.

    Works without VB-Cable or Voicemeeter.

📎 Files

    websocket_server.py – WebSocket server that listens for commands

    loopback.py – Audio capture logic for mic + system

    transcribe.py – Groq Whisper v3 API integration

    index.html – Browser control interface

    transcripts.txt – Output file (auto-created)

    .env – Your Groq API key

    requirements.txt – All Python dependencies

🎧 That’s it — open the page, hit record, and watch the transcripts appear!