from pydantic import BaseModel

class EmbeddingHistory(BaseModel):
  embedding: list[float]
  score: int
class QuestRequest(BaseModel):
  minutes: int
  location: tuple[float, float]
  embedding_history: list[EmbeddingHistory]

