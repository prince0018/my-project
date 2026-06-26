from __future__ import annotations

import hashlib
from collections.abc import Iterable, Sequence
from dataclasses import dataclass

from portfolio_chatbot.chroma_index import get_chroma_collection
from portfolio_chatbot.chunking import TextChunk, split_documents_into_chunks
from portfolio_chatbot.config import IngestionSettings, get_ingestion_settings
from portfolio_chatbot.document_loaders import iter_document_files, load_documents_from_directory
from portfolio_chatbot.embeddings import OpenAIEmbeddingService


@dataclass(frozen=True)
class IngestionResult:
    source_file_count: int
    source_document_count: int
    chunk_count: int
    collection_name: str
    collection_document_count: int


def ingest_documents(settings: IngestionSettings | None = None) -> IngestionResult:
    settings = settings or get_ingestion_settings()

    source_files = iter_document_files(settings.docs_path)
    source_documents = load_documents_from_directory(settings.docs_path)
    chunks = split_documents_into_chunks(
        source_documents,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )

    collection = get_chroma_collection()

    if chunks:
        embedding_service = OpenAIEmbeddingService(model=settings.embedding_model)

        for chunk_batch in _batched(chunks, settings.embedding_batch_size):
            texts = [chunk.text for chunk in chunk_batch]
            embeddings = embedding_service.embed_texts(texts)

            collection.upsert(
                ids=[_chunk_id(chunk) for chunk in chunk_batch],
                documents=texts,
                embeddings=embeddings,
                metadatas=[chunk.metadata for chunk in chunk_batch],
            )

    return IngestionResult(
        source_file_count=len(source_files),
        source_document_count=len(source_documents),
        chunk_count=len(chunks),
        collection_name=collection.name,
        collection_document_count=collection.count(),
    )


def _chunk_id(chunk: TextChunk) -> str:
    source = chunk.metadata.get("source", "unknown")
    page = chunk.metadata.get("page", "")
    chunk_index = chunk.metadata.get("chunk_index", "")
    raw_id = f"{source}|{page}|{chunk_index}|{chunk.text}"

    return hashlib.sha256(raw_id.encode("utf-8")).hexdigest()


def _batched(items: Sequence[TextChunk], batch_size: int) -> Iterable[list[TextChunk]]:
    if batch_size < 1:
        raise ValueError("OPENAI_EMBEDDING_BATCH_SIZE must be greater than 0")

    for index in range(0, len(items), batch_size):
        yield list(items[index : index + batch_size])
