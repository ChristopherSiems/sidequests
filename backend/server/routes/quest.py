from json import load
from random import choices

from fastapi import APIRouter

from backend.server.models.quest import Quest
from backend.server.models.quest_request import QuestRequest

router = APIRouter()


@router.post("/quest", response_model=Quest)
async def quest(quest_request: QuestRequest):
  quest = None
  with open("backend/server/dummy_quests.json") as f:
    quest = choices([Quest(**quest) for quest in load(f)])[0]

  return quest
