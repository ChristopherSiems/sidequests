import json
import os
import sqlite3
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.."))
from backend.database import init_db
from backend.scraper.llm_client import test_connection
from backend.scraper.scrape_engage import get_posts as get_engage_posts
from backend.scraper.scrape_culture import get_posts as get_culture_posts


def _save_to_db(posts, db_path):
  init_db(db_path)
  con = sqlite3.connect(db_path)
  cur = con.cursor()
  cur.execute("DELETE FROM events")
  cur.executemany(
    """
		INSERT INTO events
		(title, link, description, categories, image, start_time, end_time, location, latitude, longitude, min_time, embedding)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
	""",
    [
      (
        post.get("title"),
        post.get("link"),
        post.get("description"),
        ", ".join(post.get("categories", [])),
        post.get("image"),
        post.get("start"),
        post.get("end"),
        post.get("location"),
        post.get("latitude") or 42.250713,
        post.get("longitude") or -71.822836,
        post.get("min_time", 0),
        json.dumps(post.get("embedding", [])),
      )
      for post in posts
      if post.get("min_time", 0) > 0 and post.get("title") != "N/A"
    ],
  )
  con.commit()
  con.close()


def scrape():
  if not test_connection():
    return

  engage_posts = get_engage_posts()
  culture_posts = get_culture_posts()
  print(f"[Scraper] Fetched {len(engage_posts)} engage + {len(culture_posts)} culture posts")

  all_posts = engage_posts + culture_posts
  db_path = os.path.join(os.path.dirname(__file__), "../data/quests.db")
  _save_to_db(all_posts, db_path)
  print(f"[Scraper] Saved {len(all_posts)} total posts to events table")


if __name__ == "__main__":
  scrape()
