# agents/keyword_explainer_agent.py

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class KeywordExplainerAgent:
    def __init__(self, model_name="llama-3.3-70b-versatile"):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment.")
        self.client = Groq(api_key=self.api_key)
        self.model_name = model_name

    def run(self, transcript: str) -> list:
        """
        Extract and explain keywords from the transcript using LLM.
        Returns a list of dicts: [{'keyword': ..., 'definition': ...}, ...]
        """
        prompt = (
            f"""You are an assistant that explains buzzwords found in a transcript.
            Read the following transcript and return a list of keywords along with their short, simple definitions.\n\n
            Transcript:\n{transcript}\n\n
            Return the response in this format:\n
            - keyword: <word>, definition: <short explanation>"""
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that explains complex terms simply."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )

            answer = response.choices[0].message.content.strip()
            return self._parse_keywords(answer)

        except Exception as e:
            print("❌ Keyword extraction failed:", e)
            return []

    def _parse_keywords(self, raw_text: str) -> list:
        """
        Parse LLM output into structured list of keywords with definitions.
        """
        lines = raw_text.strip().splitlines()
        keywords = []
        for line in lines:
            if "- keyword:" in line:
                parts = line.split(", definition:")
                if len(parts) == 2:
                    keyword = parts[0].replace("- keyword:", "").strip()
                    definition = parts[1].strip()
                    keywords.append({"keyword": keyword, "definition": definition})
        return keywords
