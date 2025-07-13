# polyglot-backend/Dockerfile
FROM python:3.12-slim-bookworm

WORKDIR /app

# Install system dependencies needed by pydub (for ffmpeg)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your custom agent code (main.py and any agent files in 'agents' folder if you moved them)
# Assuming main.py contains all agent definitions and session.register_agent calls
COPY main.py .
# If you have separate agent files in an 'agents' folder here, copy it too:
# COPY agents/ agents/

# Expose the port where your custom genai-agentos app runs
EXPOSE 8008

# Command to run your custom genai-agentos application
CMD ["python", "main.py"]