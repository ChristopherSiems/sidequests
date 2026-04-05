from random import choices

from fastapi import APIRouter

from backend.database import get_available_quests
from backend.server.models.quest import Quest
from backend.server.models.quest_request import QuestRequest
from backend.server.models.interaction_request import InteractionRequest
from backend.database import add_interaction

router = APIRouter()


@router.post("/quest", response_model=Quest | None)
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


@router.post("/interactions", response_model=None)
async def interactions(interaction_request: InteractionRequest) -> None:
  print(str(interaction_request))
  add_interaction(interaction_request.embedding, interaction_request.score)
  return None