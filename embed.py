import os
import json
import sqlite3

import numpy as np
import torch
import faiss
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

ENCODER_MODEL = os.getenv("ENCODER_MODEL")
FAISS_INDEX = os.getenv("FAISS_INDEX")
SQLITE = os.getenv("SQLITE")
TABLE = os.getenv("TABLE_NAME")


# Deprecated. Use load_sqlite instead
def __load_json(directory):
    texts = []
    notice_ids = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                    title = data["title"]
                    content = data["content"]
                    texts.append("\n".join([title, content]))
                    notice_ids.append(filename)
                except json.JSONDecodeError as e:
                    print(f"Error decoding {filename}: {e}")
    return notice_ids, texts


def load_sqlite(db, table):
    texts = []
    notice_ids = []

    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()

        db_query = f"SELECT id, title, content FROM {table}"
        cursor.execute(db_query)
        all_notice = cursor.fetchall()

    for notice in all_notice:
        notice_id, title, content = notice
        notice_ids.append(notice_id)
        texts.append("\n".join([title, content]))

    return notice_ids, texts


device = "cuda" if torch.cuda.is_available() else "cpu"
encoder = SentenceTransformer(ENCODER_MODEL, cache_folder=ENCODER_MODEL, device=device)

notice_ids, texts = load_sqlite(SQLITE, TABLE)
embeddings = encoder.encode(texts, convert_to_numpy=True, device=device)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index = faiss.IndexIDMap(index)
index.add_with_ids(embeddings, np.array(notice_ids, dtype=np.int64))
faiss.write_index(index, FAISS_INDEX)

print("Saved successfully!")
