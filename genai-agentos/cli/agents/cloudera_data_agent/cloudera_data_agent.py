import asyncio
from typing import Annotated, Dict, Any
from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext

AGENT_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmNGZiMGFlYS02NDkwLTRiNjgtOTA0MC0zZDI0NjZmYzkzMGEiLCJleHAiOjI1MzQwMjMwMDc5OSwidXNlcl9pZCI6IjY2MTI4NjU4LWE1MzItNDY0Zi1iYWRhLTI4YjI1MzMwNjE4NiJ9.RyrcqRT41NVjuAiKHqOAtyQdkKmWUBjFqpRASB7Dt8s" 
session = GenAISession(jwt_token=AGENT_JWT)

@session.bind(
    name="cloudera_data_agent",
    description="A proof-of-concept agent to log meeting metadata to Cloudera."
)
async def cloudera_data_agent(
    agent_context: GenAIContext,
    metadata: Annotated[Dict[str, Any], "JSON object with meeting metadata."],
) -> Dict[str, Any]:
    """
    This agent receives metadata and is designed to push it to a
    Cloudera Data Stream via an MCP endpoint.
    NOTE: This is a placeholder for the hackathon.
    """
    print(f"CLOUDERA AGENT (PoC): Received metadata to log -> {metadata}")
    return {"status": "SUCCESS", "message": "Data logged to Cloudera stream (simulation)."}

async def main():
    print("Cloudera Data Agent (PoC) started.")    
    await asyncio.sleep(3600) 

if __name__ == "__main__":
    asyncio.run(main())
