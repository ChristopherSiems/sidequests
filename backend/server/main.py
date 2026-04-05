from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.scraper.scrape_engage import scrape
from backend.server.routes.quest import router as quest_router


def call_scrape():
  print("scraping")
  scrape()


@asynccontextmanager
async def lifespan(app: FastAPI):
  scheduler.add_job(call_scrape, "cron", hour=22, minute=29)
  scheduler.start()
  yield
  scheduler.shutdown()


scheduler = AsyncIOScheduler()
app = FastAPI(lifespan=lifespan)

app.add_middleware(
  CORSMiddleware,
  allow_origins=[
    "http://localhost:3000",
  ],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
app.include_router(quest_router)
