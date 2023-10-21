from fastapi import APIRouter

from src.interface.models.story import Stories
from src.interface.models.story_base import StoryBase, db_dependency

stories_router = APIRouter()


@stories_router.post("/stories/")
async def create_stories(story: StoryBase, db: db_dependency):
    db_story = Stories(title=story.title, text=story.text)
    db.add(db_story)
    db.commit()
    db.refresh(db_story)
