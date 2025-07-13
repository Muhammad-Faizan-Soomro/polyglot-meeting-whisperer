# filename: summarizer_agent.py

import os
import asyncio
from typing import Annotated, Dict, Any
from groq import Groq, AsyncGroq
from dotenv import load_dotenv


from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext


load_dotenv()


AGENT_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmNGZiMGFlYS02NDkwLTRiNjgtOTA0MC0zZDI0NjZmYzkzMGEiLCJleHAiOjI1MzQwMjMwMDc5OSwidXNlcl9pZCI6IjY2MTI4NjU4LWE1MzItNDY0Zi1iYWRhLTI4YjI1MzMwNjE4NiJ9.RyrcqRT41NVjuAiKHqOAtyQdkKmWUBjFqpRASB7Dt8s" # noqa: E501
session = GenAISession(jwt_token=AGENT_JWT)



groq_client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY"))


@session.bind(
    name="summarizer_agent",
    description="A super-fast agent that generates a concise summary of a given text using Groq's Llama3 model."
)
async def summarizer_agent(
    agent_context: GenAIContext,
    text_to_summarize: Annotated[
        str,
        "The input text that needs to be summarized.",
    ],
) -> Dict[str, Any]:
    """
    This agent takes a string of text and returns a structured dictionary
    containing a concise, bullet-point summary.
    """
    
    print(f"SummarizerAgent: Received text to summarize (length: {len(text_to_summarize)} chars).")

    
    if not text_to_summarize or len(text_to_summarize.split()) < 10:
        print("SummarizerAgent: Text too short, returning default message.")
        return {
            "success": True,
            "summary_text": "The provided text is too short to generate a meaningful summary."
        }

    
    system_prompt = "You are a world-class assistant specializing in creating highly concise and impactful summaries. Your output should be in bullet points."
    user_prompt = f"Please summarize the following text into 2-3 key bullet points:\n\n---\n{text_to_summarize}\n---"

    try:
    
        chat_completion = await groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            model="llama3-8b-8192", 
            temperature=0.5,
            max_tokens=256,
        )
        
        summary = chat_completion.choices[0].message.content
        print("SummarizerAgent: Summary generated successfully via Groq.")
        
        
        return {
            "success": True,
            "summary_text": summary
        }

    except Exception as e:
        error_message = f"SummarizerAgent: Error communicating with Groq API: {str(e)}"
        print(error_message)
        return {
            "success": False,
            "error": error_message
        }



async def main():
    print(f"SummarizerAgent with token '{AGENT_JWT[:15]}...' started. Listening for events...")
    await session.process_events()

if __name__ == "__main__":
    asyncio.run(main())