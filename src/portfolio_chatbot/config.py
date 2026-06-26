from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv(dotenv_path=ENV_PATH)


@dataclass(frozen=True)
class ChromaSettings:
    db_path: Path
    collection_name: str


@dataclass(frozen=True)
class IngestionSettings:
    docs_path: Path
    embedding_model: str
    chunk_size: int
    chunk_overlap: int
    embedding_batch_size: int


@dataclass(frozen=True)
class ChatSettings:
    chat_model: str
    retrieval_top_k: int
    max_history_turns: int


def _get_int_env(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default

    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer, got {value!r}") from exc


def get_chroma_settings() -> ChromaSettings:
    return ChromaSettings(
        db_path=Path(os.getenv("CHROMA_DB_PATH", "./chroma_db")),
        collection_name=os.getenv("CHROMA_COLLECTION_NAME", "portfolio_profile"),
    )


def get_ingestion_settings() -> IngestionSettings:
    return IngestionSettings(
        docs_path=Path(os.getenv("DOCS_PATH", "./docs")),
        embedding_model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002"),
        chunk_size=_get_int_env("CHUNK_SIZE", 1000),
        chunk_overlap=_get_int_env("CHUNK_OVERLAP", 150),
        embedding_batch_size=_get_int_env("OPENAI_EMBEDDING_BATCH_SIZE", 64),
    )


def get_chat_settings() -> ChatSettings:
    return ChatSettings(
        chat_model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"),
        retrieval_top_k=_get_int_env("RETRIEVAL_TOP_K", 4),
        max_history_turns=_get_int_env("MAX_HISTORY_TURNS", 4),
    )


def get_openai_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Create a .env file from .env.example and add your key."
        )
    if api_key == "your_openai_api_key_here":
        raise RuntimeError("OPENAI_API_KEY still has the placeholder value. Add your real key.")

    return api_key
