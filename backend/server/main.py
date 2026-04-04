from fastapi import FastAPI

from backend.server.routes.quest import router as quest_router

app = FastAPI()
app.include_router(quest_router, prefix="/quests", tags=["quests"])
