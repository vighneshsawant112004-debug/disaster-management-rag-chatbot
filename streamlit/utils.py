"""
utils.py - Shared helper utilities for DisasterAI.
"""

import re
import logging
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)


# ── Text cleaning ──────────────────────────────────────────────────────────────

def clean_text(text: str) -> str:
    """
    Remove common PDF extraction artefacts and normalise whitespace.
    """
    # Remove null bytes and non-printable characters (keep newlines/tabs)
    text = re.sub(r'[^\x09\x0A\x0D\x20-\x7E\u00A0-\uFFFF]', ' ', text)
    # Collapse multiple blank lines into one
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Collapse horizontal whitespace runs
    text = re.sub(r'[ \t]{2,}', ' ', text)
    # Strip leading/trailing whitespace from every line
    lines = [ln.strip() for ln in text.splitlines()]
    text = '\n'.join(lines)
    return text.strip()


def clean_documents(documents: list) -> list:
    """Apply clean_text to every LangChain Document's page_content."""
    for doc in documents:
        doc.page_content = clean_text(doc.page_content)
    # Drop near-empty chunks
    return [d for d in documents if len(d.page_content) > 80]


# ── File discovery ─────────────────────────────────────────────────────────────

def find_pdfs(directory: Path) -> List[Path]:
    """Return all .pdf files found recursively under *directory*."""
    pdfs = list(directory.rglob("*.pdf"))
    if not pdfs:
        logger.warning("No PDF files found in %s", directory)
    else:
        logger.info("Found %d PDF(s): %s", len(pdfs), [p.name for p in pdfs])
    return pdfs


# ── Retrieval quality ──────────────────────────────────────────────────────────

def scores_are_strong(docs_and_scores: list, threshold: float) -> bool:
    """
    Return True if at least ONE retrieved chunk clears the similarity threshold.
    docs_and_scores: list of (Document, float) tuples from FAISS similarity search.
    """
    if not docs_and_scores:
        return False
    best = max(score for _, score in docs_and_scores)
    logger.debug("Best similarity score: %.3f (threshold: %.3f)", best, threshold)
    return best >= threshold


def format_context(docs: list) -> str:
    """Concatenate retrieved document chunks into a single context string."""
    parts = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", "unknown")
        page   = doc.metadata.get("page", "?")
        parts.append(
            f"[Chunk {i} | Source: {Path(source).name}, Page {page}]\n"
            f"{doc.page_content}"
        )
    return "\n\n---\n\n".join(parts)


# ── Chat history helpers ───────────────────────────────────────────────────────

def history_to_string(history: list) -> str:
    """
    Convert Streamlit session chat history to a plain-text block.
    history items: {"role": "user"|"assistant", "content": str}
    """
    lines = []
    for msg in history[:-1]:   # exclude the latest user message
        prefix = "Human" if msg["role"] == "user" else "Assistant"
        lines.append(f"{prefix}: {msg['content']}")
    return "\n".join(lines)


# ── Logging setup ──────────────────────────────────────────────────────────────

def setup_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s – %(message)s",
        datefmt="%H:%M:%S",
        level=level,
    )
