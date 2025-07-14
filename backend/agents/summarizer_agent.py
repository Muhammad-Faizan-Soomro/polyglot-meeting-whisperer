# agents/summarizer_agent.py

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class SummarizerAgent:
    def __init__(self, model="llama-3.3-70b-versatile"):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment.")
        self.client = Groq(api_key=self.api_key)
        self.model = model

        # Internal state
        self.chunk_buffer = []
        self.last_summary = ""
        self.chunk_limit = 6
        self.summary_round = 1

        self.output_file = "summary.txt"

    def add_chunk(self, chunk: str, target_language: str = "English"):
        """Add a new transcription chunk to the buffer."""
        self.chunk_buffer.append(chunk)

        if len(self.chunk_buffer) >= self.chunk_limit:
            full_text = "\n".join(self.chunk_buffer)
            input_text = f"Previous Summary:\n{self.last_summary}\n\nNew Transcript Chunks:\n{full_text}"

            try:
                prompt = (
                    f"""You are a helpful assistant. Analyze the following transcript chunk and do the following:

                1. Generate a clear, concise summary in the original language without missing any important detail.
                2. Translate that summary into {target_language}.
                3. Identify and return a brief topic/title that best represents the main subject of this transcript.

                TRANSCRIPT:
                {input_text}

                Please return your response in the following format:

                - Summary (Original):
                <original summary>

                - Summary ({target_language}):
                <translated summary>

                - Topic:
                <topic in a few words>
                """
                )

                print(f"🧠 Summarizing round {self.summary_round}...")
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a summary generator assistant."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.5
                )

                summary = response.choices[0].message.content.strip()
                self.save_summary(summary)
                self.last_summary = summary
                self.chunk_buffer.clear()
                self.summary_round += 1

                print(f"✅ Summary {self.summary_round - 1} saved.")
                return summary

            except Exception as e:
                print("❌ Summarization failed:", e)
                return ""

        return None  # Not enough chunks yet

    def save_summary(self, summary: str):
        """Save the generated summary to a file."""
        with open(self.output_file, "a", encoding="utf-8") as f:
            f.write(f"\n--- Round {self.summary_round} Summary ---\n")
            f.write(summary + "\n")
