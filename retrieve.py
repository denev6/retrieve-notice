import os
import json
import time

import torch
import faiss
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

device = "cuda" if torch.cuda.is_available() else "cpu"
FAISS_INDEX = os.getenv("FAISS_INDEX")
ENCODER_MODEL = os.getenv("ENCODER_MODEL")
BASE_URL = os.getenv("BASE_URL")

index = faiss.read_index(FAISS_INDEX)
encoder = SentenceTransformer(ENCODER_MODEL, cache_folder=ENCODER_MODEL, device=device)


# Deprecated. Use parse_sqlite instead.
def __parse_json(filename):
    DATA_DIR = os.getenv("JSON_DIR")
    path = os.path.join(DATA_DIR, filename)
    with open(path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data["title"], data["content"]


def parse_sqlite(cursor, table, notice_id):
    db_query = f"SELECT title, content FROM {table} WHERE id = ?"
    cursor.execute(db_query, (int(notice_id),))
    return cursor.fetchone()


def retrieve(query, k):
    query_embedding = encoder.encode(query, device=device).reshape(1, -1)
    distances, indices = index.search(query_embedding, k)
    return distances[0], indices[0]


def iter_retrieve_for_streamlit(cursor, table, query, k=3):
    start = time.time()
    _, notice_ids = retrieve(query, k)
    for idx, notice_id in enumerate(notice_ids, start=1):
        parsed = parse_sqlite(cursor, table, notice_id)
        if parsed is None:
            yield f"Notice {notice_id} is not found."
            continue

        title, content = parsed
        yield f"#### {idx}. {title}"
        yield f"- 링크: {BASE_URL}?mode=view&articleNo={notice_id}"
        yield f"{content}"

    end = time.time()
    yield f"[{str(device).upper()}]검색 완료: {end - start:.3f}초."


if __name__ == "__main__":
    import sqlite3

    SQLITE = os.getenv("SQLITE")
    TABLE = os.getenv("TABLE_NAME")

    with sqlite3.connect(SQLITE) as conn:
        cursor = conn.cursor()
        if cursor.connection is None:
            raise ValueError("Database connection is closed!")

        query = "의료 인공지능 마이크로디그리"
        for info in iter_retrieve_for_streamlit(cursor, TABLE, query, k=2):
            print(info)
