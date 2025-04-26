import os, pickle
from functools import lru_cache
from typing import List, Dict

MODEL_DIR = "uploads/"

@lru_cache(maxsize=32)
def load_model(path: str):
    # cargar pickle una sola vez para evitar memory leaks :contentReference[oaicite:1]{index=1} :contentReference[oaicite:2]{index=2}
    with open(path, "rb") as f:
        return pickle.load(f)

def list_model_files() -> List[str]:
    return [f for f in os.listdir(MODEL_DIR) if f.endswith((".p", ".pickle"))]
