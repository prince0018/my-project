from __future__ import annotations

from chromadb import PersistentClient
from chromadb.api.models.Collection import Collection

from portfolio_chatbot.config import ChromaSettings, get_chroma_settings


def get_chroma_collection(settings: ChromaSettings | None = None) -> Collection:
    settings = settings or get_chroma_settings()
    settings.db_path.mkdir(parents=True, exist_ok=True)

    client = PersistentClient(path=str(settings.db_path))
    return client.get_or_create_collection(
        name=settings.collection_name,
        metadata={"description": "Personal portfolio knowledge base"},
    )


def describe_chroma_collection(settings: ChromaSettings | None = None) -> dict[str, str | int]:
    settings = settings or get_chroma_settings()
    collection = get_chroma_collection(settings)

    return {
        "db_path": str(settings.db_path),
        "collection_name": collection.name,
        "document_count": collection.count(),
    }
