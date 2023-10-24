from typing import Optional

from pydantic import BaseModel

from src.infra.database import engine
from src.interface.models import story

story.Base.metadata.create_all(bind=engine)


class StoryBase(BaseModel):
    id: int
    title: str
    text: str

    class Config:
        orm_mode = True


class CreateStoryBase(BaseModel):
    title: str
    text: str


class UpdateStoryBase(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None
