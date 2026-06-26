from __future__ import annotations

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from portfolio_chatbot.ingestion import ingest_documents


def main() -> None:
    try:
        result = ingest_documents()
    except RuntimeError as exc:
        raise SystemExit(f"Error: {exc}") from exc

    print("Document ingestion finished.")
    print(f"Source files: {result.source_file_count}")
    print(f"Extracted source documents: {result.source_document_count}")
    print(f"Chunks embedded: {result.chunk_count}")
    print(f"Collection: {result.collection_name}")
    print(f"Total documents in collection: {result.collection_document_count}")


if __name__ == "__main__":
    main()
