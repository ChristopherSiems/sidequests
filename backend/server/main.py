from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.server.routes.quest import router as quest_router

app = FastAPI()

origins = [
  "http://localhost:3000",
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(quest_router)
