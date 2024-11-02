from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal
from .agents import OpenAIAgent, GeminiAgent
from .agent_tools import get_tools_config

app = FastAPI()

# Define request model
class PromptRequest(BaseModel):
    prompt: str
    agent: Literal["openai", "gemini"]

# Initialize agents with tools
tools_list = []
tools_map = {"web_search": web_search}
SYSTEM_INSTRUCTIONS = """You are a helpful AI assistant. When asked questions, provide clear and concise responses."""

# Cache agents
agents = {
    "writing_review": OpenAIAgent(
        instructions="You are a helpful assistant that reviews writing samples and provides feedback.",
        tools_list=None,
        tools_map=None
    ),
    "gemini": GeminiAgent(
        instructions=SYSTEM_INSTRUCTIONS,
        tools_map=tools_map
    )
}

@app.post("/chat")
async def chat(request: PromptRequest):
    try:
        if request.agent == "openai":
            response = agents["openai"].run_message(request.prompt)
        else:  # gemini
            response = agents["gemini"].submit(request.prompt)
            
        return {"response": response}
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
