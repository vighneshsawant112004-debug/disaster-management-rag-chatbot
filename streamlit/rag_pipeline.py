"""
rag_pipeline.py - Core RAG engine for DisasterAI.
- If PDF context is strong  → answer from documents (RAG mode)
- If PDF context is weak    → answer from LLM general knowledge (fallback mode)
- Always gives an answer, never refuses disaster/safety questions
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Tuple

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from config import (
    DATA_DIR, INDEX_DIR,
    EMBEDDING_MODEL,
    CHUNK_SIZE, CHUNK_OVERLAP,
    TOP_K, SIMILARITY_THRESHOLD,
    GROQ_API_KEY, GROQ_MODEL, LLM_MAX_TOKENS, LLM_TEMPERATURE,
)
from prompts import (
    RAG_SYSTEM_PROMPT, RAG_HUMAN_TEMPLATE,
    FALLBACK_SYSTEM_PROMPT, FALLBACK_HUMAN_TEMPLATE,
    CONDENSE_PROMPT,
)
from utils import (
    find_pdfs, clean_documents,
    scores_are_strong, format_context,
    history_to_string, setup_logging,
)

setup_logging()
logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════════════════
# 1. Document Loading & Chunking
# ══════════════════════════════════════════════════════════════════════════════

def load_and_chunk_documents(data_dir: Path = DATA_DIR) -> List[Document]:
    pdfs = find_pdfs(data_dir)
    raw_docs: List[Document] = []
    for pdf_path in pdfs:
        try:
            loader = PyPDFLoader(str(pdf_path))
            raw_docs.extend(loader.load())
        except Exception as exc:
            logger.warning("Failed to load %s: %s", pdf_path.name, exc)

    cleaned = clean_documents(raw_docs)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(cleaned)
    logger.info("Total chunks: %d", len(chunks))
    return chunks


# ══════════════════════════════════════════════════════════════════════════════
# 2. Embeddings
# ══════════════════════════════════════════════════════════════════════════════

def get_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


# ══════════════════════════════════════════════════════════════════════════════
# 3. FAISS Vector Store
# ══════════════════════════════════════════════════════════════════════════════

def build_or_load_vectorstore(
    embeddings: HuggingFaceEmbeddings,
    index_dir: Path = INDEX_DIR,
    data_dir: Path = DATA_DIR,
    force_rebuild: bool = False,
) -> FAISS | None:
    """Returns None if no PDFs found — fallback-only mode."""
    index_dir.mkdir(parents=True, exist_ok=True)
    index_file = index_dir / "index.faiss"

    if index_file.exists() and not force_rebuild:
        try:
            vs = FAISS.load_local(
                str(index_dir), embeddings,
                allow_dangerous_deserialization=True,
            )
            logger.info("FAISS index loaded (%d chunks).", vs.index.ntotal)
            return vs
        except Exception as exc:
            logger.warning("Could not load index (%s); rebuilding…", exc)

    pdfs = find_pdfs(data_dir)
    if not pdfs:
        logger.warning("No PDFs found — running in fallback-only mode.")
        return None

    chunks = load_and_chunk_documents(data_dir)
    vs = FAISS.from_documents(chunks, embeddings)
    vs.save_local(str(index_dir))
    logger.info("FAISS index built and saved (%d chunks).", vs.index.ntotal)
    return vs


# ══════════════════════════════════════════════════════════════════════════════
# 4. LLM — Groq (free tier, no credit card needed)
# ══════════════════════════════════════════════════════════════════════════════

def get_llm() -> ChatGroq:
    if not GROQ_API_KEY:
        raise EnvironmentError(
            "GROQ_API_KEY is not set.\n"
            "Get a FREE key at https://console.groq.com → API Keys\n"
            "Then add it to your .env file: GROQ_API_KEY=your_key_here"
        )
    return ChatGroq(
        api_key=GROQ_API_KEY,
        model_name=GROQ_MODEL,
        max_tokens=LLM_MAX_TOKENS,
        temperature=LLM_TEMPERATURE,
    )


# ══════════════════════════════════════════════════════════════════════════════
# 5. Question condensing (multi-turn)
# ══════════════════════════════════════════════════════════════════════════════

def condense_question(llm: ChatGroq, question: str, history: list) -> str:
    if not history:
        return question
    history_str = history_to_string(history)
    prompt_text = CONDENSE_PROMPT.format(
        chat_history=history_str,
        question=question,
    )
    try:
        resp = llm.invoke([HumanMessage(content=prompt_text)])
        return resp.content.strip() or question
    except Exception:
        return question


# ══════════════════════════════════════════════════════════════════════════════
# 6. Core answer function — ALWAYS returns an answer
# ══════════════════════════════════════════════════════════════════════════════

def answer_with_rag(
    llm: ChatGroq,
    vectorstore: FAISS | None,
    question: str,
) -> Tuple[str, str]:
    """
    Three-tier answering strategy:
    Tier 1 — RAG:      PDF docs have strong match → answer from documents
    Tier 2 — Hybrid:   PDF docs have weak match   → LLM uses docs as hints + own knowledge
    Tier 3 — Fallback: No PDFs / no match at all  → LLM answers from own knowledge freely
    ALWAYS returns an answer. Never says "I don't know" for safety/disaster topics.
    """

    # ── Tier 3: No vector store (no PDFs loaded) ──────────────────────────────
    if vectorstore is None:
        logger.info("No vectorstore — pure LLM fallback.")
        system_msg = SystemMessage(content=FALLBACK_SYSTEM_PROMPT)
        human_msg  = HumanMessage(content=FALLBACK_HUMAN_TEMPLATE.format(question=question))
        response   = llm.invoke([system_msg, human_msg])
        return response.content.strip(), "fallback"

    # ── Retrieve chunks ────────────────────────────────────────────────────────
    try:
        docs_and_scores: List[Tuple[Document, float]] = \
            vectorstore.similarity_search_with_score(question, k=TOP_K)
    except Exception as e:
        logger.warning("FAISS search error: %s — pure fallback.", e)
        docs_and_scores = []

    # ── Tier 1: Strong RAG ────────────────────────────────────────────────────
    if scores_are_strong(docs_and_scores, SIMILARITY_THRESHOLD):
        docs    = [d for d, _ in docs_and_scores]
        context = format_context(docs)
        system_msg = SystemMessage(content=RAG_SYSTEM_PROMPT.format(context=context))
        human_msg  = HumanMessage(content=RAG_HUMAN_TEMPLATE.format(question=question))
        response   = llm.invoke([system_msg, human_msg])
        return response.content.strip(), "rag"

    # ── Tier 2 & 3: Fallback — LLM answers freely from its own knowledge ──────
    # This covers EVERYTHING: snake bites, first aid, survival, NDMA, psychology,
    # international guidelines, region-specific advice, out-of-the-box queries, etc.
    logger.info("Weak/no retrieval — free LLM fallback (covers all safety topics).")
    system_msg = SystemMessage(content=FALLBACK_SYSTEM_PROMPT)
    human_msg  = HumanMessage(content=FALLBACK_HUMAN_TEMPLATE.format(question=question))
    response   = llm.invoke([system_msg, human_msg])
    return response.content.strip(), "fallback"


# ══════════════════════════════════════════════════════════════════════════════
# 7. Public pipeline entry-point
# ══════════════════════════════════════════════════════════════════════════════

class DisasterAIPipeline:
    """
    Main pipeline. Works in two modes:
    - Full mode:     PDFs found → builds FAISS index → RAG + fallback
    - Fallback-only: No PDFs   → pure LLM (still answers everything)
    """

    def __init__(self, force_rebuild: bool = False):
        self.embeddings  = get_embeddings()
        self.vectorstore = build_or_load_vectorstore(
            self.embeddings, force_rebuild=force_rebuild
        )
        self.llm = get_llm()

        if self.vectorstore is None:
            logger.info("DisasterAI running in FALLBACK-ONLY mode (no PDFs).")
        else:
            logger.info("DisasterAI pipeline ready (RAG + fallback).")

    @property
    def mode(self) -> str:
        return "full" if self.vectorstore else "fallback-only"

    def ask(self, question: str, chat_history: list | None = None) -> dict:
        history    = chat_history or []
        standalone = condense_question(self.llm, question, history)
        answer, mode = answer_with_rag(self.llm, self.vectorstore, standalone)
        return {
            "answer": answer,
            "mode":   mode,
            "standalone_question": standalone,
        }

    def rebuild_index(self) -> None:
        self.vectorstore = build_or_load_vectorstore(
            self.embeddings, force_rebuild=True
        )