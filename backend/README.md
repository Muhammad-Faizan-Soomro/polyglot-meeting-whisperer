# 🧠 Polyglot Meeting Whisperer

**Polyglot Meeting Whisperer** is a real-time meeting assistant that captures microphone audio in chunks, transcribes it, translates it, summarizes it, and generates questions — all using AI agents.

## 📁 Project Structure

```bash
.
├── backend/
│   ├── index.html
│   ├── websocket_server.py
│   └── agents/
│       ├── transcribe_agent.py
│       ├── translate_agent.py
        ├── keyword_explainer_agent.py
│       ├── summarizer_agent.py
│       └── question_generator_agent.py
```

## 🔧 Backend

### `websocket_server.py`
Main server that:
- Listens for WebSocket connections
- Accepts 5-second microphone audio chunks
- Saves chunks to temporary `.webm` files
- Processes files through AI agent pipeline:
  - 📝 **TranscribeAgent**
  - 🌍 **TranslateAgent**
  - 📚 **SummarizerAgent**
  - ❓ **QuestionGeneratorAgent**
  - 🧠 **KeywordExplanationAgent**
- Saves transcripts, translations and keywords explanation to `transcripts.txt`
- Saves summaries to `summary.txt`
- Saves questions to `questions.txt`

Uses an **asynchronous queue-based pipeline** to process chunks concurrently without data loss.

## 🤖 AI Agents

All agents use Groq API and are located in `backend/agents/`

### `transcribe_agent.py`
- Uses **Groq Whisper v3**
- Converts audio files to text

### `translate_agent.py`
- Uses **Groq LLM (LLaMA-3)**
- Translates text to any language (default: Spanish)

### `summarizer_agent.py`
- Buffers transcripts in groups (e.g., 6 chunks = summary of pas 30 seconds)
- Summarizes content using Groq LLM
- Return summaries in both languages ( original + user-comfortable )

### `keyword_explainer_agent.py`
- Detects buzzwords or technical terms in the transcript and explains them in 1–2 simple lines.
- Appended to transcripts.txt after each chunk.

### `question_generator_agent.py`
- Generates insightful questions based on summaries
- Outputs saved to `questions.txt`

## 🌐 Frontend

### `index.html`
Minimal test page with:
- ▶️ **Start Recording** button
- ⏹️ **Stop Recording** button
- Handles microphone capture and WebSocket streaming

## 🚀 Running the Frontend
Avoid `file://` restrictions by using a local server:

```bash
cd backend
python -m http.server 8000
```
Access at:  
`http://localhost:8000/`

## 🗂 Output Files
- `transcripts.txt`: Chunk-by-chunk transcripts, translations and keyword explanation
- `summary.txt`: Summaries
- `questions.txt`: Generated questions

## ✅ Requirements
- Python 3.9+
- Dependencies in `requirements.txt`
- `.env` file with `GROQ_API_KEY`
