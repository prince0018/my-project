from __future__ import annotations

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from portfolio_chatbot.chroma_index import describe_chroma_collection


def main() -> None:
    details = describe_chroma_collection()

    print("ChromaDB index is ready.")
    print(f"Path: {details['db_path']}")
    print(f"Collection: {details['collection_name']}")
    print(f"Documents: {details['document_count']}")


if __name__ == "__main__":
    main()
