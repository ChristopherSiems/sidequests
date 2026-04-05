from json import load

from database import create_POI
from scraper.embed import attach_embeddings_to_quests

quests = []
with open("POIs.json") as f:
  quests = load(f)

quests = attach_embeddings_to_quests(quests)
for quest in quests:
  create_POI(
    **{k: v for k, v in quest.items() if k != "id"}, db_path="backend/data/quests.db"
  )
