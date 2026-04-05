from pydantic import BaseModel


class POICreate(BaseModel):
  title: str
  description: str
  location: str
  latitude: float
  longitude: float
  open_time: str
  close_time: str
  min_time: int  # seconds
  day: str
  categories: str = ""
  image: str = ""
  link: str = ""
