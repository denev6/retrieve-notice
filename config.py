import os
import argparse

import torch
from sentence_transformers import SentenceTransformer
from dotenv import set_key, load_dotenv

ENV_PATH = ".env"

if not os.path.exists(ENV_PATH):
    raise FileNotFoundError(f"{ENV_PATH} not found.")

load_dotenv(ENV_PATH)

# Save Openai API key
parser = argparse.ArgumentParser(description="Config .env file")
parser.add_argument("--openai", help="OpenAI API Key", required=True)
args = parser.parse_args()

set_key(ENV_PATH, "OPENAI_KEY", args.openai)

# Save encoder
ENCODER = os.getenv("ENCODER_MODEL")

device = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer(ENCODER, device=device)
model.save(ENCODER)
