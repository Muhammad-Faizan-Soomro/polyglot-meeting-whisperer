# filename: translator_agent.py

import os
import json
import asyncio
from typing import Annotated, List, Dict, Any
from groq import Groq, AsyncGroq
from dotenv import load_dotenv

from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext


load_dotenv()

AGENT_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlMjU1MTU2MC1hNmQzLTQ1NDktOTMxYy1jNjA2NDU4MjdhZWYiLCJleHAiOjI1MzQwMjMwMDc5OSwidXNlcl9pZCI6IjY2MTI4NjU4LWE1MzItNDY0Zi1iYWRhLTI4YjI1MzMwNjE4NiJ9.IXbrMtglKp_v3IGG_O435Sv0uSgEjl2cfR-lRg4hnwk" # noqa: E501
session = GenAISession(jwt_token=AGENT_JWT)


groq_client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY"))

@session.bind(
    name="translator_agent",
    description="A high-speed agent that translates text into multiple languages using Groq."
)
async def translator_agent(
    agent_context: GenAIContext,
    text_to_translate: Annotated[
        str,
        "The text content that needs translation.",
    ],
    target_languages: Annotated[
        List[str],
        "A list of languages to translate the text into, e.g., ['Chinese', 'French', 'Arabic']",
    ]
) -> Dict[str, Any]:
    """
    This agent takes a text and a list of languages, and returns a dictionary
    with the translations.
    """
    if not text_to_translate:
        return {"success": True, "translations": {lang: "" for lang in target_languages}}

    print(f"TranslatorAgent: Received task to translate to {target_languages}.")
    

    system_prompt = """You are an expert multilingual translator. Your task is to translate the provided text into several languages.
You MUST return the output as a single, valid JSON object, where the keys are the language names and the values are the translated text.
Do not include any other text, explanations, or markdown formatting. Just the JSON object.
Example format: {"Chinese": "你好世界", "French": "Bonjour le monde"}"""
    
    user_prompt = f"""Please translate the following text into these languages: {json.dumps(target_languages)}.

Text to translate:
"{text_to_translate}"
"""
    
    try:
        chat_completion = await groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            model="llama3-70b-8192", 
            temperature=0.2,
            max_tokens=1024,
            response_format={"type": "json_object"}, 
        )
        
        response_content = chat_completion.choices[0].message.content
        translations = json.loads(response_content)
        
        print(f"TranslatorAgent: Translations generated successfully via Groq: {translations}")
        
        return {
            "success": True,
            "translations": translations
        }
        
    except Exception as e:
        error_message = f"TranslatorAgent: Error with Groq API or JSON parsing: {str(e)}"
        print(error_message)
        return {
            "success": False,
            "error": error_message
        }



async def main():
    print(f"TranslatorAgent with token '{AGENT_JWT[:15]}...' started. Listening for events...")
    await session.process_events()

if __name__ == "__main__":
    asyncio.run(main())