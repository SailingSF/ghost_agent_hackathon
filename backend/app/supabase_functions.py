# nothing here yet
import supabase
import os
from data_models import User, Story, StoryOutline, StoryPart
from datetime import datetime

def get_supabase_client():
    return supabase.create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

async def get_user_by_id(id: int) -> User:
    client = get_supabase_client()
    data = client.table("users").select("*").eq("id", id).execute().data[0]
    return User(**data)

async def get_stories_by_user_id(user_id: int) -> list[Story]:
    client = get_supabase_client()
    data = client.table("stories").select("*").eq("user_id", user_id).execute().data
    return [Story(**story) for story in data]

async def create_story_part(story_part: StoryPart) -> StoryPart:
    client = get_supabase_client()
    story_part_dict = story_part.model_dump(exclude={'id'})
    data = client.table("story_parts").insert(story_part_dict).execute().data[0]
    return StoryPart(**data)

async def create_story(story: Story) -> Story:
    client = get_supabase_client()
    story_dict = story.model_dump(exclude={'id', 'outline'})
    story_dict['created_at'] = story_dict['created_at'].isoformat()
    
    data = client.table("stories").insert(story_dict).execute().data[0]
    data['created_at'] = datetime.fromisoformat(data['created_at'])
    return Story(**data, outline=None)

async def update_story(story: Story) -> Story:
    client = get_supabase_client()
    story_dict = story.model_dump(exclude={'outline'})
    story_dict['created_at'] = story_dict['created_at'].isoformat()
    
    data = client.table("stories").update(story_dict).eq("id", story.id).execute().data[0]
    data['created_at'] = datetime.fromisoformat(data['created_at'])
    return Story(**data, outline=story.outline)

async def create_story_outline(story_outline: StoryOutline) -> StoryOutline:
    client = get_supabase_client()
    outline_dict = story_outline.model_dump(exclude={'id'})
    data = client.table("story_outlines").insert(outline_dict).execute().data[0]
    return StoryOutline(**data)

async def update_story_outline(story_outline: StoryOutline) -> StoryOutline:
    client = get_supabase_client()
    outline_dict = story_outline.model_dump()
    data = client.table("story_outlines").update(outline_dict).eq("id", story_outline.id).execute().data[0]
    return StoryOutline(**data)