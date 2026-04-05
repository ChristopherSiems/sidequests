import sqlite3
from contextlib import contextmanager
import datetime
import math

DB_PATH = "quests.db"

@contextmanager
def get_connection(db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

#initializes db
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
                min_time    INTEGER NOT NULL
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
                min_time    INTEGER NOT NULL
            );
        """)
    print(f"Database initialised at '{db_path}'.")

#enters an event into the db
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
    db_path: str = DB_PATH,
) -> int:
    with get_connection(db_path) as conn:
        cur = conn.execute(
            """
            INSERT INTO events (title, link, description, categories, image, start_time, end_time, location, latitude, longitude, min_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (title, link, description, categories, image, start_time, end_time, location, latitude, longitude, min_time),
        )
    return cur.lastrowid

#enters a permanent into the db, one row per day of operation
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
    db_path: str = DB_PATH,
) -> int:
    with get_connection(db_path) as conn:
        cur = conn.execute(
            """
            INSERT INTO POIs (title, link, description, categories, image, open_time, close_time, day, location, latitude, longitude, min_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (title, link, description, categories, image, open_time, close_time, day, location, latitude, longitude, min_time),
        )
    return cur.lastrowid

# haversine formula: calculates straight line distance in km between two coordinate pairs in degrees
def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return R * 2 * math.asin(math.sqrt(a))

# estimates walking travel time in minutes assuming 5km/h
def _travel_minutes(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    return (_haversine_km(lat1, lon1, lat2, lon2) / 5) * 60

# takes in [free_time] in minutes, user coordinates, and finds all overlapping time quests from both
# tables that the user can reasonably reach and spend [min_time] at before returning.
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
            SELECT id, title, link, description, categories, image, location, latitude, longitude, min_time FROM events
            WHERE start_time < ? AND end_time > ?
            UNION
            SELECT id, title, link, description, categories, image, location, latitude, longitude, min_time FROM POIs
            WHERE day = ? AND open_time < ? AND close_time > ?
            ORDER BY title
            """,
            (end_unix, now_unix, current_day, end_time, current_time),
        ).fetchall()

    results = []
    for row in rows:
        quest = dict(row)
        travel_time = _travel_minutes(user_lat, user_lon, quest["latitude"], quest["longitude"])
        if (travel_time * 2) + quest["min_time"] <= free_time:
            results.append(quest)

    return results
