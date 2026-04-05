from pydantic import BaseModel

class InteractionRequest(BaseModel):
  embedding: list[float]
  score: int