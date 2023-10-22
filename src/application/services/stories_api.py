from fastapi import APIRouter, HTTPException, status
from sqlalchemy import exc

from src.interface.models.story import Stories
from src.interface.models.story_base import StoryBase, db_dependency

stories_router = APIRouter()


@stories_router.get("/stories/")
async def list_stories(db: db_dependency):
    result = db.query(Stories).all()
    return result


@stories_router.post("/stories/", status_code=status.HTTP_201_CREATED)
async def create_stories(story: StoryBase, db: db_dependency):
    db_story = Stories(title=story.title, text=story.text)
    try:
        db.add(db_story)
        db.commit()
        db.refresh(db_story)
    except exc.DBAPIError as e:
        detail = e.orig.diag.message_detail
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
    return db_story
