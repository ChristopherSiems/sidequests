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
            CREATE TABLE IF NOT EXISTS quests (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT    NOT NULL,
                link        TEXT,
                description TEXT,
                categories  TEXT,
                image       TEXT,
                start_time  INTEGER NOT NULL,
                end_time    INTEGER NOT NULL,
                location    TEXT
            );
        """)
    print(f"Database initialised at '{db_path}'.")

#enters a quest into the db
def create_quest(
    title: str,
    start_time: int,
    end_time: int,
    link: str = "",
    description: str = "",
    categories: str = "",
    image: str = "",
    location: str = "",
    db_path: str = DB_PATH,
) -> int:
    with get_connection(db_path) as conn:
        cur = conn.execute(
            """
            INSERT INTO quests (title, link, description, categories, image, start_time, end_time, location)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (title, link, description, categories, image, start_time, end_time, location),
        )
    return cur.lastrowid

# takes in [free_time], the int representation of the duration the user is free in seconds.
# Finds all quests in the db that overlap with the time the user is free and returns them in
# a list of dictionaries.
def get_available_quests(free_time: int, db_path: str = DB_PATH) -> list:
    now = int(datetime.datetime.now().timestamp())
    end = now + (free_time * 60)

    with get_connection(db_path) as conn:
        rows = conn.execute(
            """
            SELECT * FROM quests
            WHERE start_time < ? AND end_time > ?
            ORDER BY start_time
            """,
            (end, now),
        ).fetchall()

    return [dict(r) for r in rows]

#tests
# if __name__ == "__main__":
#     import os

#     DB = "dev_quests.db"
#     if os.path.exists(DB):
#         os.remove(DB)

#     init_db(DB)

#     now = int(datetime.datetime.now().timestamp())
#     hour = 3600

#     create_quest(
#         title="Hackathon",
#         start_time=now - hour,
#         end_time=now + hour,
#         location="Engineering Hall",
#         db_path=DB,
#     )
#     create_quest(
#         title="Campus Coffee House",
#         start_time=now - (12 * hour),
#         end_time=now + (12 * hour),
#         location="Student Union",
#         db_path=DB,
#     )
#     create_quest(
#         title="Already Over",
#         start_time=now - (2 * hour),
#         end_time=now - 1,
#         location="Nowhere",
#         db_path=DB,
#     )

#     results = get_available_quests(free_time=30, db_path=DB)
#     titles = [q["title"] for q in results]
#     print(f"Results: {titles}")

#     assert "Hackathon" in titles, "FAIL: hackathon missing"
#     assert "Campus Coffee House" in titles, "FAIL: coffee house missing"
#     assert "Already Over" not in titles, "FAIL: ended quest should be excluded"

#     print("All checks passed ✓")
#     os.remove(DB)