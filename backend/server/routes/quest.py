from random import choices

from fastapi import APIRouter

from backend.database import get_available_quests
from backend.server.models.quest import Quest
from backend.server.models.quest_request import QuestRequest

router = APIRouter()


@router.post("/quest", response_model=Quest)
async def quests(quest_request: QuestRequest) -> Quest | list:
  print(str(quest_request))

  quests = get_available_quests(
    quest_request.minutes,
    quest_request.location[0],
    quest_request.location[1],
    db_path="backend/data/quests.db",
  )

  if quests == []:
    return None

  print("quests", quests)
  quest = choices(quests)

  print("quest", quest)
  if quest == []:
    return None

  return Quest(
    start_time=quest[0]["start_time"],
    end_time=quest[0]["end_time"],
    location=quest[0]["location"],
    title=quest[0]["title"],
    link=quest[0]["link"],
  )
