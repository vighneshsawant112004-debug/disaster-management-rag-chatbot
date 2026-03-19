"""
config.py - Central configuration for DisasterAI RAG pipeline.
All tuneable parameters in one place for easy scaling and maintenance.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent.parent          # project root
DATA_DIR   = BASE_DIR / "data"                     # PDF source folder
INDEX_DIR  = BASE_DIR / "streamlit" / "faiss_index"  # persisted FAISS index

# ── Embedding model ────────────────────────────────────────────────────────────
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ── Text-splitting ─────────────────────────────────────────────────────────────
CHUNK_SIZE    = 800   # characters per chunk
CHUNK_OVERLAP = 150   # overlap to preserve context across chunk boundaries

# ── Retrieval ──────────────────────────────────────────────────────────────────
TOP_K                = 5     # chunks returned per query
SIMILARITY_THRESHOLD = 0.20  # cosine-similarity floor; below → fallback LLM

# ── Groq / LLM ────────────────────────────────────────────────────────────────
GROQ_API_KEY    = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL      = "llama-3.3-70b-versatile"
LLM_MAX_TOKENS  = 1024
LLM_TEMPERATURE = 0.2

# ── UI ─────────────────────────────────────────────────────────────────────────
APP_TITLE    = "DisasterAI"
APP_SUBTITLE = "Emergency Guidance · Powered by RAG"
APP_ICON     = "🆘"