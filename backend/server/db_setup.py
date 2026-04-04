from json import load

from backend.server.models.quest import Quest
from backend.database import create_quest, get_available_quests, init_db

if __name__ == "__main__":
  init_db()

  quests = []
  with open("backend/server/dummy_quests.json") as f:
    for quest in [Quest(**quest) for quest in load(f)]:
      create_quest(
        quest.title,
        quest.start_time,
        quest.end_time,
        location=str(quest.location),
        link=quest.link,
      )

  print(get_available_quests(99999999))
