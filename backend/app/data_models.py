from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str

class Story(BaseModel):
    id: int
    title: str
    user_id: int
    created_at: datetime
    outline: StoryOutline

class StoryOutline(BaseModel):
    id: int
    title: str
    themes: list[str]
    characters: list[str]
    setting: str
    plot_points: list[str]

class StoryPart(BaseModel):
    id: int
    story_id: int
    part_number: int
    content: str

