from fastapi import FastAPI
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitSDK, Action as CopilotAction
from agents import GeminiAgent, OpenAIAgent
import google.generativeai as genai
from openai import OpenAI
from agent_tools import web_search
import weave
from pydantic import BaseModel
import typing_extensions as typing
import os
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = FastAPI()
 
# Define your backend action
@weave.op(name="get_news_summary")
async def get_news_summary(query: str):
    tools_map = {"web_search": web_search}
    agent = GeminiAgent(instructions="You are a helpful assistant that retrieves current news.", tools_map=tools_map)
    response = agent.submit(query)
    return response
 
# this is a dummy action for demonstration purposes
action_get_news = CopilotAction(
    name="get_news",
    description="Fetches a news summary from the web given a search query.",
    parameters=[
        {
            "name": "query",
            "type": "string",
            "description": "The search query to fetch news for.",
            "required": True,
        }
    ],
    handler=get_news_summary
)
 
# Initialize the CopilotKit SDK
sdk = CopilotKitSDK(actions=[action_get_news])
 
# Add the CopilotKit endpoint to your FastAPI app
add_fastapi_endpoint(app, sdk, "/copilotkit")

@weave.op(name="create_written_story")
async def create_written_story(notes: str):
    genai.configure(api_key=os.environ["GOOGLE_GEMINI_API_KEY"])
    model = genai.GenerativeModel(model_name="gemini-1.5-pro", system_instruction="You are a helpful assistant that creates a well-written story based on the provided notes and outline. You return just the story, no other text.")
    prompt = f"Create a well-written story based on the following notes and outline in JSON format: {notes}\n\nYour story will be in raw text and 500 words."
    response = model.generate_content(prompt)

    return response.text

class StoryRequest(BaseModel):
    notes: str

class StoryOutline(BaseModel):
    title: str
    themes: list[str]
    characters: list[str]
    setting: str
    plot_points: list[str]

class StoryOutlineRequest(BaseModel):
    conversation: str
    previous_outline: str

@app.post("/write_story")
async def write_story(request: StoryRequest):
    weave.init('ghost-agent')
    story = await create_written_story(request.notes)
    return {"story": story}

@weave.op(name="create_story_outline")
@app.post("/create_story_outline")
async def create_story_outline(request: StoryOutlineRequest) -> dict:
    weave.init('ghost-agent')

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])   
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini", 
        messages=[
            {"role": "system", "content": "You are a helpful assistant that creates a story outline based on the provided notes. You return just the outline in JSON format with title, themes, characters, setting, and plot_points fields. Return every specified field."},
            {"role": "user", "content": f"""This is the previous outline:\n{request.previous_outline}\n\n
            Create a new story outline by filling in the required fields for the outline.
            
            Return a JSON object with these exact fields:
            - title: string
            - themes: array of strings
            - characters: array of strings
            - setting: string
            - plot_points: array of strings
            
            Incorporate the newest information from the following conversation:\n\n {request.conversation}
            """}
        ],
        response_format=StoryOutline
    )
    return {"outline": completion.choices[0].message.parsed}

def main():
    """Run the uvicorn server."""
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
 
if __name__ == "__main__":
    main()