import os

import torch
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv("../.env")
ENCODER = os.getenv("ENCODER_MODEL")

device = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer(ENCODER, device=device)
model.save(f"../{ENCODER}")
print(ENCODER, "saved.")

"""
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

SUMMARY = os.getenv("SUMMARY_MODEL")

model = AutoModelForSeq2SeqLM.from_pretrained(SUMMARY)
tokenizer = AutoTokenizer.from_pretrained(SUMMARY)
model.save_pretrained(f"../{SUMMARY}")
model.save_pretrained(f"../{SUMMARY}")
print(SUMMARY, "saved.")
"""
