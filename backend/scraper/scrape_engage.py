import os
import sqlite3
import sys
from datetime import datetime

import feedparser
from bs4 import BeautifulSoup

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from database import init_db
from llm_client import enrich_posts

# print(events_feed.keys())


def get_posts_details(rss=None):
<<<<<<< HEAD
  """
  Take link of rss feed as argument
  """
  if rss is not None:
    # parsing blog feed
    blog_feed = blog_feed = feedparser.parse(rss)
=======
	"""
	Take link of rss feed as argument
	"""
	if rss is not None:
		# parsing blog feed
		blog_feed = feedparser.parse(rss)
>>>>>>> 42fb093 (Begin integrating scraper with calls to local LLM)

    # getting lists of blog entries via .entries
    posts = blog_feed.entries

    # dictionary for holding posts details
    posts_details = {
      "Blog title": blog_feed.feed.title,
      "Blog link": blog_feed.feed.link,
    }

    post_list = []

    # iterating over individual posts
    for post in posts:
      temp = dict()

      # if any post doesn't have information print error message
      try:
        temp["title"] = post.title
        temp["link"] = post.link
        temp["categories"] = [tag.term for tag in post.get("tags", [])]

        dr = description_reader(post.summary)

        temp["description"] = dr.get("p-description description")

        temp["start"] = dr.get_unix_time("dt-start dtstart")
        temp["end"] = dr.get_unix_time("dt-end dtend")
        temp["location"] = dr.get("p-location location")
        temp["image"] = post.enclosures[0].url if post.get("enclosures") else None
        if (
          temp["start"] is not None
          and temp["start"] < int(datetime.now().timestamp()) + 24 * 3600
          and temp["end"] is not None
          and temp["end"] > int(datetime.now().timestamp())
        ):
          post_list.append(temp)
      except:
        print("error parsing rss")

    # storing lists of posts in the dictionary
    posts_details["posts"] = post_list

    return posts_details
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


def save_to_db(posts, db_path):
  init_db(db_path)
  con = sqlite3.connect(db_path)
  cur = con.cursor()
  cur.execute("DELETE FROM quests")
  cur.executemany(
    """
		INSERT INTO quests
		(title, link, description, categories, image, start_time, end_time, location)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?)
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
      )
      for post in posts
    ],
  )
  con.commit()
  con.close()


if __name__ == "__main__":
  feed_url = "https://engage.clarku.edu/events.rss"

  data = get_posts_details(rss=feed_url)  # return blogs data as a dictionary

  if data:
    db_path = os.path.join(os.path.dirname(__file__), "../data/events.db")
    save_to_db(data["posts"], db_path)
    # entry = data["posts"][0]
    # for key in entry.keys():
    # print(f'Key: {key}\nData: {entry[key]}\n')

  else:
    print("None")
