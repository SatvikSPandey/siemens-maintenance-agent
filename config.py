import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).parent

DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"
VECTOR_STORE_PATH = Path("C:/Users/babaw/faiss_store")
MANUALS_DIR = DATA_DIR / "manuals"
EQUIPMENT_DB_PATH = DATA_DIR / "equipment.db"
CHECKPOINT_DB_PATH = DATA_DIR / "checkpoints.db"

OLLAMA_MODEL = "llama3"
OLLAMA_BASE_URL = "http://localhost:11434"

COHERE_LLM_MODEL = "command-r-plus-08-2024"

import socket
def is_ollama_running():
    try:
        sock = socket.create_connection(("localhost", 11434), timeout=2)
        sock.close()
        return True
    except:
        return False

IS_STREAMLIT_CLOUD = os.getenv("HOME") == "/home/adminuser"
USE_OLLAMA = False if IS_STREAMLIT_CLOUD else is_ollama_running()

try:
    import streamlit as st
    COHERE_API_KEY = st.secrets["COHERE_API_KEY"]
except Exception:
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
COHERE_EMBEDDING_MODEL = "embed-english-v3.0"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
RAG_TOP_K = 4

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_STORE_PATH.mkdir(parents=True, exist_ok=True)
MANUALS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)