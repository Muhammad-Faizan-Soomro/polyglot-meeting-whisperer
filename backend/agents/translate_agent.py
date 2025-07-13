# agents/translate_agent.py

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class TranslateAgent:
    def __init__(self, model_name="llama-3.3-70b-versatile"):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment.")
        self.client = Groq(api_key=self.api_key)
        self.model_name = model_name

    def run(self, text: str, target_language: str = "English") -> str:
        """
        Translate the given English text to the specified target language.
        Returns the translated text, or an empty string on failure.
        """
        try:
            prompt = f"Translate the following English text to {target_language}:\n\n{text}\n\nReturn only translation."
            print(f"🌐 TranslateAgent: Translating to {target_language}")
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name
            )
            translated_text = response.choices[0].message.content.strip()
            print(f"🌍 Translated Text: {translated_text}")
            return translated_text
        except Exception as e:
            print("❌ Translation failed:", e)
            return ""
