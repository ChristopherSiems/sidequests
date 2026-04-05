from fastapi import APIRouter

from backend.database import get_available_quests
from backend.server.models.quest import Quest
from backend.server.models.quest_request import QuestRequest
from backend.server.models.interaction_request import InteractionRequest
from backend.database import add_interaction
from backend.recommender.recommender import get_best_quest
router = APIRouter()


@router.post("/quest", response_model=Quest | None)
async def quests(quest_request: QuestRequest) -> Quest | list:

  quests = get_available_quests(
    quest_request.minutes,
    quest_request.location[0],
    quest_request.location[1],
    db_path="backend/data/quests.db",
  )
  print("quests----", len(quests))
  if quests == []:
    return None

  
  quest = get_best_quest(quests, quest_request.embedding_history)


  if quest is None:
    return None

  return Quest(
    start_time=quest["start_time"],
    end_time=quest["end_time"],
    location=quest["location"],
    title=quest["title"],
    link=quest["link"],
    embedding=quest["embedding"],
  )


@router.post("/interactions", response_model=None)
async def interactions(interaction_request: InteractionRequest) -> None:
  print(str(interaction_request))
  add_interaction(interaction_request.embedding, interaction_request.score)
  return None