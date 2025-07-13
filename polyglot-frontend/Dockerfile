# polyglot-gradio-frontend/Dockerfile
FROM python:3.12-slim-bookworm

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Gradio application code
COPY app.py .

# Expose the port where Gradio runs
EXPOSE 7860

# Command to run the Gradio application
CMD ["python", "app.py"]