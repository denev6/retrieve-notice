import os
import json
import time

import torch
import faiss
from sentence_transformers import SentenceTransformer
import openai
from dotenv import load_dotenv

load_dotenv()

device = "cuda" if torch.cuda.is_available() else "cpu"
FAISS_INDEX = os.getenv("FAISS_INDEX")
ENCODER_MODEL = os.getenv("ENCODER_MODEL")
BASE_URL = os.getenv("BASE_URL")
OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")

index = faiss.read_index(FAISS_INDEX)
encoder = SentenceTransformer(ENCODER_MODEL, cache_folder=ENCODER_MODEL, device=device)


def summarize(user_query, references, model="gpt-3.5-turbo"):
    client = openai.OpenAI(api_key=OPENAI_TOKEN)

    references = "\n".join(
        [f"doc {i + 1}: '{references[i]}'" for i in range(len(references))]
    )
    system_prompt = f"""You are an assistant that specialized in summarizing and answering documents about school notices.
    You need to take given documents and return a detailed summary.
    Here are the documents:
    {references}
    You must answer in Korean based on the documents.
    """

    user_prompt = f"User question: '{str(user_query.strip())}'."
    prompt = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    response = client.chat.completions.create(
        model=model,
        messages=prompt,
        temperature=0.3,
        max_tokens=500,
    )
    return response.choices[0].message.content


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


def iter_retriever_for_testing(cursor, table, query, k=3):
    start = time.time()
    _, notice_ids = retrieve(query, k)
    for idx, notice_id in enumerate(notice_ids, start=1):
        parsed = parse_sqlite(cursor, table, notice_id)
        if parsed is None:
            yield f"Notice {notice_id} is not found."
            continue

        title, content = parsed
        yield f"## {idx}. {title}"
        yield f"- 링크: {BASE_URL}?mode=view&articleNo={notice_id}"
        yield f"{content}"

    end = time.time()
    yield f"[{str(device).upper()}]검색 완료: {end - start:.3f}초."


def ask_chatgpt_with_references(cursor, table, query, k=3):
    start = time.time()
    _, notice_ids = retrieve(query, k)
    references = []
    notice_links = []
    for notice_id in notice_ids:
        parsed = parse_sqlite(cursor, table, notice_id)
        if parsed is None:
            print(f"Notice {notice_id} is not found.")
            continue

        title, content = parsed
        references.append(f"{title}: {content}")
        notice_links.append(f"- {BASE_URL}?mode=view&articleNo={notice_id}")

    gpt_response = summarize(query, references)

    end = time.time()
    notice_links = "\n".join(notice_links)
    duration = f"[{str(device).upper()}]검색 완료: {end - start:.3f}초."

    return gpt_response, notice_links, duration


if __name__ == "__main__":
    import sqlite3

    SQLITE = os.getenv("SQLITE")
    TABLE = os.getenv("TABLE_NAME")

    with sqlite3.connect(SQLITE) as conn:
        cursor = conn.cursor()
        if cursor.connection is None:
            raise ValueError("Database connection is closed!")

        query = "의료 인공지능 마이크로디그리"
        for info in iter_retriever_for_testing(cursor, TABLE, query, k=2):
            print(info)
