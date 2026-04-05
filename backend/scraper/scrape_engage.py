import os
import sqlite3
import sys
from datetime import datetime
import json
from backend.scraper.embed import attach_embeddings_to_quests
from backend.scraper.get_coordinates import get_coordinates

import feedparser
from bs4 import BeautifulSoup

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from backend.database import init_db

from backend.scraper.llm_client import questify_posts, test_connection

_PROMPT_PATH = os.path.join(os.path.dirname(__file__), "questgiver_prompt.md")
with open(_PROMPT_PATH, "r") as f:
  _SYSTEM_PROMPT = f.read()


def _get_posts_details(rss=None):
  """
  Take link of rss feed as argument
  """
  if rss is not None:
    # parsing blog feed
    blog_feed = feedparser.parse(rss)

    # getting lists of blog entries via .entries
    posts = blog_feed.entries

    post_list = []

    # iterating over individual posts
    for post in posts:
      temp = dict()

      # if any post doesn't have information print error message
      try:
        temp["title"] = post.title
        temp["link"] = post.link
        temp["host"] = post.host
        temp["categories"] = [tag.term for tag in post.get("tags", [])]

        dr = description_reader(post.summary)

        temp["description"] = dr.get("p-description description")

        raw_loc = dr.get("p-location location")
        lat, lon, clean_address = get_coordinates(raw_loc)
        temp["location"] = clean_address
        temp["latitude"] = lat
        temp["longitude"] = lon


        temp["start"] = dr.get_unix_time("dt-start dtstart")
        temp["end"] = dr.get_unix_time("dt-end dtend")
        temp["image"] = post.enclosures[0].url if post.get("enclosures") else None
        if (
          temp["start"] is not None
          and temp["start"] < int(datetime.now().timestamp()) + 28 * 3600
          and temp["end"] is not None
          and temp["end"] > int(datetime.now().timestamp())
          and temp["end"] - temp["start"] < 48 * 3600
        ):
          post_list.append(temp)
      except Exception as e:
        print(f"[Scraper] Error parsing RSS feed: {e}")

    return post_list
  else:
    return None


class description_reader:
  soup: BeautifulSoup

  def __init__(self, description):
    self.soup = BeautifulSoup(description, "html.parser")

  def get(self, content):
    # Extract text from any tag with the given class
    elements = self.soup.find_all(True, class_=content)
    return "\n".join(el.get_text(separator=" ", strip=True) for el in elements)

  def get_unix_time(self, content):
    ev_time = self.soup.find("time", class_=content)
    if ev_time and ev_time.get("datetime"):
      return int(datetime.fromisoformat(ev_time["datetime"]).timestamp())
    return None


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
        post.get("latitude"),
        post.get("longitude"),
        post.get("min_time", 0),
        json.dumps(post.get("embedding", []))
      )
      for post in posts
      if post.get("min_time", 0) > 0 and post.get("title") != "N/A"
    ],
  )
  con.commit()
  con.close()


_CATEGORY_MULTIPLIERS = {
  "no-commitment": 0.1,
  "light-commitment": 0.25,
  "moderate-commitment": 0.5,
  "full-commitment": 1.0,
}


def _apply_min_time(posts):
  for post in posts:
    start = post.get("start")
    end = post.get("end")
    category = post.get("time_category")
    multiplier = _CATEGORY_MULTIPLIERS.get(category)
    if start is not None and end is not None and multiplier is not None:
      post["min_time"] = int((end - start) * multiplier)
    else:
      post["min_time"] = 0
  return posts


def get_posts(feed_url="https://engage.clarku.edu/events.rss"):
  data = _get_posts_details(rss=feed_url)
  if data is None:
    return []
  data = questify_posts(data, system_prompt=_SYSTEM_PROMPT)
  data = _apply_min_time(data)
  return attach_embeddings_to_quests(data)


def scrape(feed_url="https://engage.clarku.edu/events.rss"):
  if test_connection():
    data = get_posts(feed_url)
    db_path = os.path.join(os.path.dirname(__file__), "../data/quests.db")
    _save_to_db(data, db_path)


if __name__ == "__main__":
  scrape()
