import os
import json
import sqlite3

from dotenv import load_dotenv

load_dotenv("../.env")

JSON_DIR = f"../{os.getenv('JSON_DIR')}"
SQLITE = f"../{os.getenv('SQLITE')}"
TABLE = os.getenv("TABLE_NAME")

conn = sqlite3.connect(SQLITE)
cursor = conn.cursor()

db_query = f"""
    CREATE TABLE IF NOT EXISTS {TABLE} (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        content TEXT NOT NULL
    )
"""
cursor.execute(db_query)
conn.commit()


def insert(notice_id, title, content):
    try:
        db_query = f"INSERT INTO {TABLE} (id, title, content) VALUES (?, ?, ?)"
        cursor.execute(
            db_query,
            (notice_id, title, content),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Error: ID {notice_id} already exists.")


for filename in os.listdir(JSON_DIR):
    if filename.endswith(".json"):
        file_path = os.path.join(JSON_DIR, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            title = data["title"]
            content = data["content"]
            idx = int(filename.rsplit(".", 1)[0])
            insert(idx, title, content)

conn.close()
