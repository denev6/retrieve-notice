import os
import sqlite3

import streamlit as st
from dotenv import load_dotenv

from retrieve import ask_chatgpt_with_references

load_dotenv()

SQLITE = os.getenv("SQLITE")
TABLE = os.getenv("TABLE_NAME")


with sqlite3.connect(SQLITE) as conn:
    cursor = conn.cursor()
    if cursor.connection is None:
        raise ValueError("Database connection is closed!")

    st.title("학교 공지 검색")
    query = st.text_input("입력")
    btn_search = st.button("검색")
    text_holder = st.empty()

    if btn_search:
        text_holder.write("검색 중...🐕")
        result = ask_chatgpt_with_references(cursor, TABLE, query, k=3)
        text_holder.write("\n".join(result))
