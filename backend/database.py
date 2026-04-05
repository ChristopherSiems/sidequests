import datetime
import json
import math
import os
import sqlite3
from contextlib import contextmanager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "quests.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def _migrate_global_interactions(conn: sqlite3.Connection) -> None:
    cols = {row[1] for row in conn.execute("PRAGMA table_info(global_interactions)")}
    if cols and "quest_id" not in cols:
        conn.execute("ALTER TABLE global_interactions ADD COLUMN quest_id INTEGER")


@contextmanager
def get_connection(db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        try:
            _migrate_global_interactions(conn)
        except sqlite3.OperationalError:
            pass
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# initializes db
def init_db(db_path: str = DB_PATH):
  with get_connection(db_path) as conn:
    conn.executescript("""
            CREATE TABLE IF NOT EXISTS events (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT    NOT NULL,
                link        TEXT,
                description TEXT,
                categories  TEXT,
                image       TEXT,
                start_time  INTEGER NOT NULL,
                end_time    INTEGER NOT NULL,
                location    TEXT,
                latitude    REAL    NOT NULL,
                longitude   REAL    NOT NULL,
                min_time    INTEGER NOT NULL,
                embedding   TEXT    -- NEW: Stores JSON stringified vector array
            );
            CREATE TABLE IF NOT EXISTS POIs (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT    NOT NULL,
                link        TEXT,
                description TEXT,
                categories  TEXT,
                image       TEXT,
                open_time   TEXT    NOT NULL,
                close_time  TEXT    NOT NULL,
                day         TEXT    NOT NULL CHECK(day IN (
                                'Monday','Tuesday','Wednesday',
                                'Thursday','Friday','Saturday','Sunday'
                            )),
                location    TEXT,
                latitude    REAL    NOT NULL,
                longitude   REAL    NOT NULL,
                min_time    INTEGER NOT NULL,
                embedding   TEXT    -- NEW: Stores JSON stringified vector array
            );
            
            CREATE TABLE IF NOT EXISTS global_interactions (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                embedding   TEXT    NOT NULL,
                score       INTEGER    NOT NULL,
                quest_id    INTEGER
            );
        """)
  print(f"Database initialised at '{db_path}'.")


# takes embedding and score and adds to the db
def add_interaction(
    embedding: list,
    score: int,
    quest_id: int | None = None,
    db_path: str = DB_PATH,
) -> int:
    embedding_str = json.dumps(embedding)

    with get_connection(db_path) as conn:
        cur = conn.execute(
            """
            INSERT INTO global_interactions (embedding, score, quest_id)
            VALUES (?, ?, ?)
            """,
            (embedding_str, score, quest_id),
        )
    return cur.lastrowid


# enters an event into the db (Updated to handle embedding)
def create_event(
  title: str,
  start_time: int,
  end_time: int,
  location: str,
  latitude: float,
  longitude: float,
  min_time: int,
  link: str = "",
  description: str = "",
  categories: str = "",
  image: str = "",
  embedding: list = None,
  db_path: str = DB_PATH,
) -> int:
  if embedding is None:
    embedding = []
  embedding_str = json.dumps(embedding)

  with get_connection(db_path) as conn:
    cur = conn.execute(
      """
            INSERT INTO events (title, link, description, categories, image, start_time, end_time, location, latitude, longitude, min_time, embedding)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
      (
        title,
        link,
        description,
        categories,
        image,
        start_time,
        end_time,
        location,
        latitude,
        longitude,
        min_time,
        embedding_str,
      ),
    )
  return cur.lastrowid


# enters a permanent into the db (Updated to handle embedding)
def create_POI(
  title: str,
  day: str,
  open_time: str,
  close_time: str,
  location: str,
  latitude: float,
  longitude: float,
  min_time: int,
  link: str = "",
  description: str = "",
  categories: str = "",
  image: str = "",
  embedding: list = None,
  db_path: str = DB_PATH,
) -> int:
  if embedding is None:
    embedding = []
  embedding_str = json.dumps(embedding)

  with get_connection(db_path) as conn:
    cur = conn.execute(
      """
            INSERT INTO POIs (title, link, description, categories, image, open_time, close_time, day, location, latitude, longitude, min_time, embedding)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
      (
        title,
        link,
        description,
        categories,
        image,
        open_time,
        close_time,
        day,
        location,
        latitude,
        longitude,
        min_time,
        embedding_str,
      ),
    )
  return cur.lastrowid


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
  R = 6371
  lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
  dlat = lat2 - lat1
  dlon = lon2 - lon1
  a = (
    math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
  )
  return R * 2 * math.asin(math.sqrt(a))


def _travel_minutes(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
  return (_haversine_km(lat1, lon1, lat2, lon2) / 5) * 60


# Updated to fetch the embedding and parse it back to a python list
def get_available_quests(
  free_time: int,
  user_lat: float,
  user_lon: float,
  db_path: str = DB_PATH,
) -> list:
  now = datetime.datetime.now()
  now_unix = int(now.timestamp())
  end_unix = now_unix + (free_time * 60)
  current_day = now.strftime("%A")
  current_time = now.strftime("%H:%M")
  end_time = (now + datetime.timedelta(minutes=free_time)).strftime("%H:%M")

  with get_connection(db_path) as conn:
    rows = conn.execute(
      """
            SELECT id, title, link, description, categories, image, location, latitude, longitude, min_time, start_time, end_time, embedding FROM events
            WHERE start_time < ? AND end_time > ?
            UNION
            SELECT id, title, link, description, categories, image, location, latitude, longitude, min_time, open_time, close_time, embedding FROM POIs
            WHERE day = ? AND open_time < ? AND close_time > ?
            ORDER BY title
            """,
      (end_unix, now_unix, current_day, end_time, current_time),
    ).fetchall()

  results = []
  for row in rows:
    quest = dict(row)

    quest["embedding"] = json.loads(quest["embedding"]) if quest["embedding"] else []
    print(quest["title"])

    travel_time = _travel_minutes(
      user_lat, user_lon, quest["latitude"], quest["longitude"]
    )

    print("travel_time", (travel_time * 2))
    print("min_time", quest["min_time"] / 60)
    print("free_time", free_time)
    if (travel_time * 2) + quest["min_time"] / 60 <= free_time:
      results.append(quest)

  return results


# grabs all glboal interactions
def get_global_interactions(db_path: str = DB_PATH) -> list:
    with get_connection(db_path) as conn:
        rows = conn.execute(
            """
            SELECT embedding, score, quest_id FROM global_interactions
            """
    ).fetchall()

  results = []
  for row in rows:
    interaction = dict(row)
    interaction["embedding"] = (
      json.loads(interaction["embedding"]) if interaction["embedding"] else []
    )
    results.append(interaction)

  return results

