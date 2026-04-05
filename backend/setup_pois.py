from json import load

from database import create_POI

with open("POIs.json") as f:
  for quest in load(f):
    create_POI(
      **{k: v for k, v in quest.items() if k != "id"}, db_path="backend/data/quests.db"
    )
