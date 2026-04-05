import json
import os
import re
import sqlite3
import sys
from datetime import datetime

import feedparser
import requests
from bs4 import BeautifulSoup

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from backend.database import init_db

from backend.scraper.llm_client import questify_posts, test_connection
from backend.scraper.embed import attach_embeddings_to_quests

_PROMPT_PATH = os.path.join(os.path.dirname(__file__), "questgiver_culture_prompt.md")
with open(_PROMPT_PATH, "r") as f:
  _SYSTEM_PROMPT = f.read()


def _parse_date_range(description_html):
  """
  Extract start and end unix timestamps from DiscoverCentralMA description HTML.
  Handles "MM/DD/YYYY to MM/DD/YYYY" and "Starting MM/DD/YYYY" text patterns.
  """
  soup = BeautifulSoup(description_html, "html.parser")
  text = soup.get_text()

  # Pattern: "MM/DD/YYYY to MM/DD/YYYY"
  range_match = re.search(r"(\d{2}/\d{2}/\d{4})\s+to\s+(\d{2}/\d{2}/\d{4})", text)
  if range_match:
    start_dt = datetime.strptime(range_match.group(1), "%m/%d/%Y")
    end_dt = datetime.strptime(range_match.group(2), "%m/%d/%Y").replace(
      hour=23, minute=59, second=59
    )
    return int(start_dt.timestamp()), int(end_dt.timestamp())

  # Pattern: "Starting MM/DD/YYYY"
  start_match = re.search(r"Starting\s+(\d{2}/\d{2}/\d{4})", text)
  if start_match:
    start_dt = datetime.strptime(start_match.group(1), "%m/%d/%Y")
    end_dt = start_dt.replace(hour=23, minute=59, second=59)
    return int(start_dt.timestamp()), int(end_dt.timestamp())

  return None, None


def _get_location(event_url):
  """
  Fetch an event detail page and extract location from JSON-LD structured data.
  Returns (location_str, latitude, longitude) or (None, None, None) on failure.
  """
  try:
    resp = requests.get(event_url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    for script in soup.find_all("script", type="application/ld+json"):
      data = json.loads(script.string)
      loc = data.get("location", {})
      geo = loc.get("geo", {})
      addr = loc.get("address", {})
      lat = geo.get("latitude")
      lon = geo.get("longitude")
      name = loc.get("name", "")
      street = addr.get("streetAddress", "")
      city = addr.get("addressLocality", "")
      region = addr.get("addressRegion", "")
      location_str = ", ".join(filter(None, [name, street, city, region])) or None
      if lat is not None and lon is not None:
        return location_str, float(lat), float(lon)
  except Exception as e:
    print(f"[Scraper] Could not fetch location for {event_url}: {e}")
  return None, None, None


def _get_posts_details(rss=None):
  """
  Take link of rss feed as argument.
  """
  if rss is None:
    return None

  blog_feed = feedparser.parse(rss)
  posts = blog_feed.entries
  post_list = []

  for post in posts:
    temp = dict()
    try:
      temp["title"] = post.title
      temp["link"] = post.link
      temp["host"] = ""
      temp["categories"] = [tag.term for tag in post.get("tags", [])]

      soup = BeautifulSoup(post.summary, "html.parser")

      # Extract image from <img> tag in description
      img = soup.find("img")
      temp["image"] = img["src"] if img else None

      # Strip HTML, collapse whitespace, and remove leading date range
      raw_text = soup.get_text(separator=" ", strip=True)
      clean_text = re.sub(r"\s+", " ", raw_text).strip()
      clean_text = re.sub(r"^\d{2}/\d{2}/\d{4}\s+to\s+\d{2}/\d{2}/\d{4}\s*-?\s*", "", clean_text)
      clean_text = re.sub(r"^Starting\s+\d{2}/\d{2}/\d{4}\s*-?\s*", "", clean_text)
      temp["description"] = clean_text

      temp["location"], temp["latitude"], temp["longitude"] = _get_location(post.link)

      if temp["latitude"] is None or temp["longitude"] is None:
          print(f"  [Scraper] Skipping '{temp['title']}' - No location found.")
          continue

      from backend.scraper.get_coordinates import _haversine_km, CLARK_LAT, CLARK_LON, MAX_KM
      if _haversine_km(CLARK_LAT, CLARK_LON, temp["latitude"], temp["longitude"]) > MAX_KM:
          print(f"  [Scraper] Skipping '{temp['title']}' - Location outside Worcester area.")
          continue

      temp["start"], temp["end"] = _parse_date_range(post.summary)

      now = int(datetime.now().timestamp())
      if (
        temp["start"] is not None
        and temp["start"] < now + 28 * 3600
        and temp["end"] is not None
        and temp["end"] > now
      ):
        post_list.append(temp)
    except Exception as e:
      print(f"[Scraper] Error parsing RSS feed: {e}")

  return post_list


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
        json.dumps(post.get("embedding", [])),
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


def get_posts(feed_url="https://www.discovercentralma.org/event/rss/"):
  data = _get_posts_details(rss=feed_url)
  if data is None:
    return []
  data = questify_posts(data, system_prompt=_SYSTEM_PROMPT)
  data = _apply_min_time(data)
  return attach_embeddings_to_quests(data)


def scrape(feed_url="https://www.discovercentralma.org/event/rss/"):
  if (
    test_connection()
  ):  # Check for connection to LM Studio so db isn't wiped if connection fails
    data = get_posts(feed_url)
    db_path = os.path.join(os.path.dirname(__file__), "../data/quests.db")
    _save_to_db(data, db_path)


if __name__ == "__main__":
  scrape()
