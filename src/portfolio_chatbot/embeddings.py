from __future__ import annotations

from collections.abc import Sequence

from openai import OpenAI, OpenAIError

from portfolio_chatbot.config import get_openai_api_key


class OpenAIEmbeddingService:
    def __init__(self, model: str) -> None:
        self.model = model
        self.client = OpenAI(api_key=get_openai_api_key())

    def embed_texts(self, texts: Sequence[str]) -> list[list[float]]:
        if not texts:
            return []

        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=list(texts),
            )
        except OpenAIError as exc:
            raise RuntimeError(f"OpenAI embedding request failed: {exc}") from exc

        return [item.embedding for item in sorted(response.data, key=lambda item: item.index)]
