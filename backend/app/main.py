from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
from data_models import User, Story, StoryOutline, StoryPart
from supabase_functions import get_user_by_id, create_story, create_story_outline, create_story_part, update_story, update_story_outline
from datetime import datetime
from fastapi import HTTPException

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
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

class OutlineRequest(BaseModel):
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

# Add this new request model
class CreateStoryWithOutlineRequest(BaseModel):
    user_id: int
    title: str
    outline: OutlineRequest
    content: str

@app.post("/save_story_with_outline")
async def save_story_with_outline(request: CreateStoryWithOutlineRequest) -> dict:
    try:
        # Get the user (for validation)
        try:
            user = await get_user_by_id(request.user_id)
        except Exception as e:
            logging.error(f"Error getting user: {e}")
            raise HTTPException(status_code=404, detail="User not found")
        
        # Create the story first
        story = Story(
            id=0,
            title=request.title,
            user_id=request.user_id,
            created_at=datetime.utcnow(),
            outline=None
        )
        
        try:
            created_story = await create_story(story)
        except Exception as e:
            logging.error(f"Error creating story: {e}")
            raise HTTPException(status_code=500, detail="Failed to create story")
        
        # Create the outline with story_id
        outline = StoryOutline(
            id=0,
            story_id=created_story.id,
            title=request.outline.title,
            themes=request.outline.themes,
            characters=request.outline.characters,
            setting=request.outline.setting,
            plot_points=request.outline.plot_points
        )
        
        try:
            created_outline = await create_story_outline(outline)
        except Exception as e:
            logging.error(f"Error creating outline: {e}")
            raise HTTPException(status_code=500, detail="Failed to create outline")
        
        # Create the story part
        story_part = StoryPart(
            id=0,
            story_id=created_story.id,
            part_number=1,
            content=request.content
        )
        
        try:
            created_part = await create_story_part(story_part)
        except Exception as e:
            logging.error(f"Error creating story part: {e}")
            raise HTTPException(status_code=500, detail="Failed to create story part")
        
        # Update story with the created outline
        created_story.outline = created_outline
        updated_story = await update_story(created_story)
        
        # Convert to dict and handle datetime serialization
        response_data = {
            "story": updated_story.model_dump(),
            "outline": created_outline.model_dump(),
            "part": created_part.model_dump()
        }
        
        return response_data
        
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error saving story with outline: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def main():
    """Run the uvicorn server."""
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
 
if __name__ == "__main__":
    main()