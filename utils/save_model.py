import os

import torch
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from dotenv import load_dotenv

load_dotenv("../.env")
ENCODER = os.getenv("ENCODER_MODEL")
SUMMARY = os.getenv("SUMMARY_MODEL")

device = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer(ENCODER, device=device)
model.save(f"../{os.getenv('ENCODER_MODEL')}")
print(ENCODER, "saved.")

model = AutoModelForSeq2SeqLM.from_pretrained(SUMMARY)
tokenizer = AutoTokenizer.from_pretrained(SUMMARY)
model.save_pretrained(f"../{os.getenv('SUMMARY_MODEL')}")
model.save_pretrained(f"../{os.getenv('SUMMARY_MODEL')}")
print(SUMMARY, "saved.")
