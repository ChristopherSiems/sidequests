from fastapi import FastAPI
from pydantic import BaseModel


class Quest(BaseModel):
  title: str
  link: str
  start_time: str
  end_time: str
  location: tuple[float, float]


app = FastAPI()


@app.get("/dummy", response_model=Quest)
async def dummy():
  return Quest(
    title="hello", link="hello", location=(0.0, 0.0), start_time="1PM", end_time="2PM"
  )
