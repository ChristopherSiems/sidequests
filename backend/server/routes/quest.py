from fastapi import APIRouter

from backend.server.models.quest import Quest
from backend.server.models.quest_request import QuestRequest

router = APIRouter()


@router.post("/quest", response_model=Quest)
async def quest(request: QuestRequest):
  return Quest(
    title="hello", link="hello", location=(0.0, 0.0), start_time=0, end_time=1
  )
