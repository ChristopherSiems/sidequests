from ast import literal_eval
from random import choices

from fastapi import APIRouter

from backend.server.models.quest import Quest
from backend.server.models.quest_request import QuestRequest
from backend.database import get_available_quests

router = APIRouter()


@router.post("/quest", response_model=Quest)
async def quest(quest_request: QuestRequest):
  quest = choices(get_available_quests(quest_request.minutes))[0]
  return Quest(
    title=quest["title"],
    link=quest["link"],
    start_time=quest["start_time"],
    end_time=quest["end_time"],
    location=literal_eval(quest["location"]),
  )
