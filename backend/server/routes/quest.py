from random import choices

from fastapi import APIRouter

from backend.database import get_available_quests
from backend.server.models.quest import Quest
from backend.server.models.quest_request import QuestRequest

router = APIRouter()


@router.post("/quest", response_model=Quest)
async def quests(quest_request: QuestRequest) -> Quest | list:
  print("location", str(quest_request))
  quests = choices(
    get_available_quests(
      quest_request.minutes,
      quest_request.location[0],
      quest_request.location[1],
      db_path="backend/data/quests.db",
    )
  )

  if quests == []:
    return []

  print(quests)
  return Quest(
    start_time=quests[0]["start_time"],
    end_time=quests[0]["end_time"],
    location=quests[0]["location"],
    title=quests[0]["title"],
    link=quests[0]["link"],
  )
