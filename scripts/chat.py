from __future__ import annotations

import argparse
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from portfolio_chatbot.chatbot import ChatResponse, ChatTurn, PortfolioChatbot


EXIT_COMMANDS = {"exit", "quit", "q", ":q"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Chat with your indexed portfolio documents.")
    parser.add_argument("question", nargs="*", help="Optional one-shot question to ask.")
    parser.add_argument(
        "--hide-sources",
        action="store_true",
        help="Do not print retrieved source references after each answer.",
    )
    args = parser.parse_args()

    chatbot = PortfolioChatbot()

    if args.question:
        question = " ".join(args.question).strip()
        try:
            response = chatbot.ask(question)
        except RuntimeError as exc:
            raise SystemExit(f"Error: {exc}") from exc

        _print_response(response, hide_sources=args.hide_sources)
        return

    _run_interactive_chat(chatbot, hide_sources=args.hide_sources)


def _run_interactive_chat(chatbot: PortfolioChatbot, *, hide_sources: bool) -> None:
    history: list[ChatTurn] = []

    print("Portfolio chatbot is ready. Ask a question about your uploaded documents.")
    print("Type 'exit' to stop.\n")

    while True:
        question = input("You: ").strip()
        if not question:
            continue
        if question.lower() in EXIT_COMMANDS:
            print("Bye.")
            return

        try:
            response = chatbot.ask(question, history=history)
        except RuntimeError as exc:
            print(f"\nError: {exc}\n")
            continue

        _print_response(response, hide_sources=hide_sources)
        history.append(ChatTurn(question=question, answer=response.answer))


def _print_response(response: ChatResponse, *, hide_sources: bool) -> None:
    print(f"\nAssistant: {response.answer}")

    if response.sources and not hide_sources:
        print("\nSources:")
        for source in response.sources:
            print(f"- {source}")

    print()


if __name__ == "__main__":
    main()
