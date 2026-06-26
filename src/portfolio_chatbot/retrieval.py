from __future__ import annotations

from dataclasses import dataclass

from portfolio_chatbot.chroma_index import get_chroma_collection
from portfolio_chatbot.document_loaders import MetadataValue
from portfolio_chatbot.embeddings import OpenAIEmbeddingService


@dataclass(frozen=True)
class RetrievedChunk:
    text: str
    metadata: dict[str, MetadataValue]
    distance: float | None


def retrieve_similar_chunks(
    query: str,
    *,
    embedding_model: str,
    top_k: int,
) -> list[RetrievedChunk]:
    collection = get_chroma_collection()
    collection_count = collection.count()

    if collection_count == 0:
        return []

    embedding_service = OpenAIEmbeddingService(model=embedding_model)
    query_embedding = embedding_service.embed_texts([query])[0]
    result_count = min(top_k, collection_count)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=result_count,
        include=["documents", "metadatas", "distances"],
    )

    documents = results.get("documents", [[]])[0] or []
    metadatas = results.get("metadatas", [[]])[0] or []
    distances = results.get("distances", [[]])[0] or []

    chunks: list[RetrievedChunk] = []
    for index, text in enumerate(documents):
        if not text:
            continue

        metadata = metadatas[index] if index < len(metadatas) and metadatas[index] else {}
        distance = distances[index] if index < len(distances) else None
        chunks.append(
            RetrievedChunk(
                text=text,
                metadata=dict(metadata),
                distance=distance,
            )
        )

    return chunks
