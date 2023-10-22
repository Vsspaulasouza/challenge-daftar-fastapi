from fastapi import APIRouter, HTTPException, status
from sqlalchemy import exc

from src.interface.models.story import Stories
from src.interface.models.story_base import StoryBase, UpdateStoryBase, db_dependency

stories_router = APIRouter()


@stories_router.get("/stories/")
async def read_stories(db: db_dependency):
    result = db.query(Stories).all()
    return result


@stories_router.get("/stories/{story_id}")
async def read_story(story_id: int, db: db_dependency):
    db_story = db.query(Stories).filter(Stories.id == story_id).first()
    if db_story is None:
        raise HTTPException(status_code=404, detail="Story not found")
    return db_story


@stories_router.post("/stories/", status_code=status.HTTP_201_CREATED)
async def create_story(story: StoryBase, db: db_dependency):
    db_story = Stories(title=story.title, text=story.text)
    try:
        db.add(db_story)
        db.commit()
        db.refresh(db_story)
    except exc.DBAPIError as e:
        detail = e.orig.diag.message_detail
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
    return db_story


@stories_router.put("/stories/{story_id}")
async def update_story(story_id: int, story: UpdateStoryBase, db: db_dependency):
    db_story = db.get(Stories, story_id)
    if not db_story:
        raise HTTPException(status_code=404, detail="Story not found")

    story_data = story.model_dump(exclude_unset=True)
    for key, value in story_data.items():
        setattr(db_story, key, value)

    try:
        db.add(db_story)
        db.commit()
        db.refresh(db_story)
    except exc.DBAPIError as e:
        detail = e.orig.diag.message_detail
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
    return db_story


@stories_router.delete("/stories/{story_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_story(story_id: int, db: db_dependency):
    db_story = db.get(Stories, story_id)
    if not db_story:
        raise HTTPException(status_code=404, detail="Story not found")

    db.delete(db_story)
    db.commit()
