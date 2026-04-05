from pydantic import BaseModel, Field


class Quest(BaseModel):
  location: str
  title: str
  start_time: int | str | None = None
  end_time: int | str | None = None
  link: str | None = None
  embedding: list[float] = Field(default_factory=list)
