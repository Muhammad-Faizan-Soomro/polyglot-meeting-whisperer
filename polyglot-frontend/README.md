# 🌐 Polyglot Meeting Whisperer

Real-time speech transcription, translation, and understanding in multiple languages!

## Features

- 🎙️ **Real-time Speech Recognition**: Capture and transcribe speech in real-time
- 🌍 **Multi-language Translation**: Translate English to Chinese, French, and more
- 📝 **Live Transcript**: See the original speech text as it's being transcribed
- 📊 **Automatic Summarization**: Get key points from the conversation
- ❓ **Suggested Questions**: AI-generated follow-up questions for better participation

## Architecture

This application uses a client-server architecture:

- **Frontend**: Gradio web interface for audio recording and displaying results
- **Backend**: WebSocket server with GenAI AgentOS for processing audio and generating translations, summaries, and questions

```
┌─────────────┐        WebSocket        ┌─────────────────────┐
│             │◄──────────────────────►│                     │
│  Gradio UI  │  Audio data & results   │  GenAI AgentOS      │
│  (app.py)   │                         │  (backend_example.py)│
│             │                         │                     │
└─────────────┘                         └─────────────────────┘
```

## Setup and Installation

### Prerequisites

- Python 3.8+ (3.13 recommended)
- OpenAI API key (for the backend)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/polyglot-meeting-whisperer.git
cd polyglot-meeting-whisperer
```

2. Create a virtual environment using `uv`:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
uv pip install -r requirements.txt
```

4. Create a `.env` file with your OpenAI API key and WebSocket URL:
```bash
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
echo "WEBSOCKET_URL=ws://localhost:8000/ws" >> .env
```

### Running the Application

1. Start the backend server:
```bash
python backend_example.py
```

2. In a separate terminal, start the frontend:
```bash
python app_enhanced.py
```

The application will be available at http://127.0.0.1:7860

## How to Use

1. Select the languages you want for translation from the dropdown
2. Click the "Start Listening" button to begin recording
3. Speak clearly into your microphone
4. Click "Stop Listening" when you want to process the recording
5. View the transcript, translations, summary, and suggested questions

## Technologies Used

- **Gradio**: For the interactive web interface
- **WebSocket**: For real-time communication between frontend and backend
- **OpenAI Whisper**: For speech-to-text transcription (backend)
- **OpenAI GPT**: For translations, summaries, and question generation (backend)
- **Python**: Core programming language

## Development

### Available Versions

- `app.py`: Basic version with all functionality in a single file
- `app_enhanced.py`: WebSocket client version that connects to a backend server
- `backend_example.py`: Example WebSocket server implementation

### Customizing the Backend

You can modify the WebSocket URL by setting the `WEBSOCKET_URL` environment variable or editing the `.env` file.

## License

MIT

## Acknowledgements

- OpenAI for providing the AI models
- Gradio for the easy-to-use interface framework
