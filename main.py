# import uvicorn
from fastapi import FastAPI

from src.controller.stories_api import stories_router

app = FastAPI()

app.include_router(stories_router)

# FOR DEBUG
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
