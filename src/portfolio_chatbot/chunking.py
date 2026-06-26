from __future__ import annotations

from dataclasses import dataclass

from langchain_text_splitters import RecursiveCharacterTextSplitter

from portfolio_chatbot.document_loaders import MetadataValue, SourceDocument


@dataclass(frozen=True)
class TextChunk:
    text: str
    metadata: dict[str, MetadataValue]


def split_documents_into_chunks(
    documents: list[SourceDocument],
    *,
    chunk_size: int,
    chunk_overlap: int,
) -> list[TextChunk]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunks: list[TextChunk] = []

    for document in documents:
        split_texts = splitter.split_text(document.text)

        for chunk_index, text in enumerate(split_texts):
            text = text.strip()
            if not text:
                continue

            chunks.append(
                TextChunk(
                    text=text,
                    metadata={
                        **document.metadata,
                        "chunk_index": chunk_index,
                    },
                )
            )

    return chunks
