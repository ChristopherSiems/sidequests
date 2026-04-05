from pydantic import BaseModel


class Quest(BaseModel):
  start_time: int
  end_time: int
  location: str
  title: str
  link: str | None = None
