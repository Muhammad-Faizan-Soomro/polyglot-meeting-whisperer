import asyncio
from typing import Annotated
from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

# Define the path to the summary file
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../polyglot-meeting-whisperer/backend/summary.txt"))
# Ensure the file exists

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)


AGENT_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxNDM4NDhmZS1lOGJmLTRiODUtYWQwMy1iMzBmMDdiMWY3YTciLCJleHAiOjI1MzQwMjMwMDc5OSwidXNlcl9pZCI6IjUwYzQ4Y2VhLWMxNDktNGUzMS04MDc2LTNmOTkyYjUyOTA5NiJ9.d3WjB1zbhmACYq24AliUV4w5fnQ_uvKF4mDvDMFt-k0" # noqa: E501
session = GenAISession(jwt_token=AGENT_JWT)

# ✅ Helper: Load the summary
def load_summary(file_path="summary.txt") -> str:
    if not os.path.exists(file_path):
        return "Summary not found."
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

@session.bind(
    name="summary_qa_agent",
    description="Agent that answers questions based on a summarized discussion using Groq + LLaMA"
)
async def summary_qa_agent(
    agent_context: GenAIContext,
    question: Annotated[
        str,
        "The question that the agent will answer using the content of the meeting summary.",
    ],
):
    """Agent that answers questions based on a summarized discussion or a summarized meeting.You will have to call this agent when the user asks about the summary or a meeting or any discussion. The summary is loaded from a file, and the agent then gives answers based on that summary. If there is no context given then you will have to redirect to this agent and answer question from here"""
    agent_context.logger.info(f"Received question: {question}")
    # Load the summary
    summary = load_summary(file_path)
    if not summary:
        return "No summary available to answer questions."

    # Construct prompt
    prompt = (
        f"You are an assistant answering questions based on the following summary:\n\n"
        f"{summary}\n\n"
        f"Question: {question}\nAnswer:"
    )

    # Use Groq + LLaMA to get answer
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    answer = response.choices[0].message.content.strip()
    return answer


async def main():
    print(f"Agent with token '{AGENT_JWT}' started")
    await session.process_events()

if __name__ == "__main__":
    asyncio.run(main())
