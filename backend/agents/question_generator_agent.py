# agents/question_generator_agent.py

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class QuestionGeneratorAgent:
    def __init__(self, model_name="llama-3.3-70b-versatile"):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment.")
        self.client = Groq(api_key=self.api_key)
        self.model_name = model_name

    def run(self, summary: str) -> list:
        """
        Generate 3 insightful questions from a given summary paragraph.
        Returns a list of questions.
        """
        try:
            prompt = (
                f"""You are a helpful assistant. Given the following meeting summary,
                generate 3 insightful, thought-provoking questions that someone might ask
                to explore the topic further or assess understanding.\n\n
                SUMMARY:\n{summary}\n\n
                Make sure questions are in both languages as summary. RETURN ONLY QUESTIONS.
                QUESTIONS:"""
            )

            print("🤖 Generating questions from summary...")
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a question generation assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            result = response.choices[0].message.content.strip()
            questions = [q.strip("- ").strip() for q in result.split("\n") if q.strip()]
            if not questions:
                print("⚠️ No questions generated.")
            else:
                print(f"✅ questions generated.")
            return questions
        except Exception as e:
            print("❌ Question generation failed:", e)
            return []
