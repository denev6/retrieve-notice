import os
import argparse

import torch
from sentence_transformers import SentenceTransformer
from dotenv import set_key, load_dotenv

ENV_PATH = ".env"

if not os.path.exists(ENV_PATH):
    raise FileNotFoundError(f"{ENV_PATH} not found.")

load_dotenv(ENV_PATH)

# Save Openai API token
parser = argparse.ArgumentParser(description="Config .env file")
parser.add_argument("--token", help="OpenAI API Token", required=True)
args = parser.parse_args()

set_key(ENV_PATH, "OPENAI_TOKEN", args.token)

# Save encoder
ENCODER = os.getenv("ENCODER_MODEL")

device = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer(ENCODER, device=device)
model.save(ENCODER)
