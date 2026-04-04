from pydantic import BaseModel


class Quest(BaseModel):
  title: str
  link: str
  start_time: int
  end_time: int
  location: tuple[float, float]
