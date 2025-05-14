from sentence_transformers import SentenceTransformer
from pathlib import Path
import os
import time
import sys

MODEL_IDENTIFIER = "paraphrase-multilingual-mpnet-base-v2"
CWD = Path(__file__).parent
MODEL_PATH = f"{CWD}/src/.model"

RETRIES = 3
START_INDEX = 1

is_model_available = os.path.exists(f"{MODEL_PATH}/{MODEL_IDENTIFIER}/config.json")

if is_model_available:
    print(f"Model is already locally available")
    sys.exit(0)

for i in range(START_INDEX, START_INDEX + RETRIES):
    print(f"Fetching model {MODEL_IDENTIFIER} to {MODEL_PATH}... attempt {i}/{RETRIES}")
    try:
        model = SentenceTransformer(
            "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
            token=False
        )
        print(f"Model fetched!")
        model.save(f"{MODEL_PATH}/{MODEL_IDENTIFIER}")
        break
    except Exception as e:
        if i == RETRIES:
            print(f"Error: {e}. Could not setup model after {RETRIES} attempts.")
            raise
        else:
            print(f"Error: {e}. Retrying...")
            time.sleep(5)
