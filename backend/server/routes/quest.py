from random import choices

from fastapi import APIRouter

from backend.database import get_available_quests
from backend.server.models.quest import Quest
from backend.server.models.quest_request import QuestRequest

router = APIRouter()


@router.post("/quest", response_model=Quest)
async def quest(quest_request: QuestRequest):
  return Quest(
    **choices(
      get_available_quests(
        quest_request.minutes,
        quest_request.location[0],
        quest_request.location[1],
        db_path="backend/data/quests.db",
      )
    )[0]
  )
