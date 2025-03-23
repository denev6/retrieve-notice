import os
import sqlite3

import streamlit as st
from dotenv import load_dotenv

from retrieve import iter_retrieve_for_streamlit

load_dotenv()

SQLITE = os.getenv("SQLITE")
TABLE = os.getenv("TABLE_NAME")


with sqlite3.connect(SQLITE) as conn:
    cursor = conn.cursor()
    if cursor.connection is None:
        raise ValueError("Database connection is closed!")

    st.title("학교 공지 검색")
    query = st.text_input("입력: ")

    if st.button("검색"):
        for info in iter_retrieve_for_streamlit(cursor, TABLE, query):
            st.markdown(info)
