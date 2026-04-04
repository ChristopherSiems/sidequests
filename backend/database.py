import sqlite3
from contextlib import contextmanager
import datetime

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
                location    TEXT    NOT NULL
            );
            CREATE TABLE IF NOT EXISTS permanents (
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
                location    TEXT    NOT NULL
            );
        """)
    print(f"Database initialised at '{db_path}'.")

#enters an event into the db
def create_event(
    title: str,
    location: str,
    start_time: int,
    end_time: int,
    link: str = "",
    description: str = "",
    categories: str = "",
    image: str = "",
    db_path: str = DB_PATH,
) -> int:
    with get_connection(db_path) as conn:
        cur = conn.execute(
            """
            INSERT INTO events (title, link, description, categories, image, start_time, end_time, location)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (title, link, description, categories, image, start_time, end_time, location),
        )
    return cur.lastrowid

#enters a permanent into the db, one row per day of operation
def create_permanent(
    title: str,
    day: str,
    open_time: str,
    close_time: str,
    location: str,
    link: str = "",
    description: str = "",
    categories: str = "",
    image: str = "",
    db_path: str = DB_PATH,
) -> int:
    with get_connection(db_path) as conn:
        cur = conn.execute(
            """
            INSERT INTO permanents (title, link, description, categories, image, open_time, close_time, day, location)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (title, link, description, categories, image, open_time, close_time, day, location),
        )
    return cur.lastrowid

# takes in [free_time], the int representation of the duration the user is free in minutes.
# Finds all quests in both tables that overlap with the time the user is free and returns them
# in a list of dictionaries.
def get_available_quests(free_time: int, db_path: str = DB_PATH) -> list:
    now = datetime.datetime.now()
    now_unix = int(now.timestamp())
    end_unix = now_unix + (free_time * 60)
    current_day = now.strftime("%A")
    current_time = now.strftime("%H:%M")
    end_time = (now + datetime.timedelta(minutes=free_time)).strftime("%H:%M")

    with get_connection(db_path) as conn:
        rows = conn.execute(
            """
            SELECT id, title, link, description, categories, image, location FROM events
            WHERE start_time < ? AND end_time > ?
            UNION
            SELECT id, title, link, description, categories, image, location FROM permanents
            WHERE day = ? AND open_time < ? AND close_time > ?
            ORDER BY title
            """,
            (end_unix, now_unix, current_day, end_time, current_time),
        ).fetchall()

    return [dict(r) for r in rows]