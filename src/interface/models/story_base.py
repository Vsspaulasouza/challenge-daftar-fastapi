from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.interface.dto.database import SessionLocal, engine
from src.interface.models import story

story.Base.metadata.create_all(bind=engine)


class StoryBase(BaseModel):
    title: str
    text: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
