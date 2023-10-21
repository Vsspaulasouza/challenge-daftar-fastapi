from fastapi import FastAPI

from src.application.services.stories_api import stories_router

app = FastAPI()

app.include_router(stories_router)
