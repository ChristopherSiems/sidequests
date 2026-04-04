from pydantic import BaseModel


class QuestRequest(BaseModel):
  minutes: int
  location: tuple[float, float]
