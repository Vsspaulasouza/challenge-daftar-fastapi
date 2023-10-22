from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import exc
from sqlalchemy.orm import Session

from src.interface.dto.database import get_session
from src.interface.models.story import Stories
from src.interface.models.story_base import CreateStoryBase, StoryBase, UpdateStoryBase

stories_router = APIRouter()


@stories_router.get("/stories/", response_model=List[StoryBase])
def read_stories(*, session: Session = Depends(get_session)):
    result = session.query(Stories).all()
    return result


@stories_router.get("/stories/{story_id}", response_model=StoryBase)
async def read_story(*, session: Session = Depends(get_session), story_id: int):
    db_story = session.query(Stories).filter(Stories.id == story_id).first()
    if db_story is None:
        raise HTTPException(status_code=404, detail="Story not found")
    return db_story


@stories_router.post("/stories/", response_model=StoryBase, status_code=status.HTTP_201_CREATED)
async def create_story(*, session: Session = Depends(get_session), story: CreateStoryBase):
    db_story = Stories(title=story.title, text=story.text)
    try:
        session.add(db_story)
        session.commit()
        session.refresh(db_story)
    except exc.DBAPIError as e:
        detail = e.orig.diag.message_detail
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
    return db_story


@stories_router.put("/stories/{story_id}", response_model=StoryBase)
async def update_story(*, session: Session = Depends(get_session), story_id: int, story: UpdateStoryBase):
    db_story = session.get(Stories, story_id)
    if not db_story:
        raise HTTPException(status_code=404, detail="Story not found")

    story_data = story.model_dump(exclude_unset=True)
    for key, value in story_data.items():
        setattr(db_story, key, value)

    try:
        session.add(db_story)
        session.commit()
        session.refresh(db_story)
    except exc.DBAPIError as e:
        detail = e.orig.diag.message_detail
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
    return db_story


@stories_router.delete("/stories/{story_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_story(*, session: Session = Depends(get_session), story_id: int):
    db_story = session.get(Stories, story_id)
    if not db_story:
        raise HTTPException(status_code=404, detail="Story not found")

    session.delete(db_story)
    session.commit()
