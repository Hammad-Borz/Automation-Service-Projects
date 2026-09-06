"""Embedding providers with a replaceable interface."""

from __future__ import annotations

import hashlib
import math
import re
from typing import Protocol

from .exceptions import EmbeddingError
from .logger import get_logger

_TOKEN = re.compile(r"[a-z0-9]+")


class EmbeddingProvider(Protocol):
    dimension: int

    def embed_query(self, text: str) -> list[float]: ...

    def embed_documents(self, texts: list[str]) -> list[list[float]]: ...


class HashingEmbeddingProvider:
    """Local hashed n-gram embeddings for demo mode and tests.

    Vectors are deterministic and require no external API. They are suitable
    for lexical retrieval on small knowledge bases, not for production semantic search.
    """

    def __init__(self, dimension: int = 256) -> None:
        if dimension < 32:
            raise EmbeddingError("Embedding dimension must be at least 32.")
        self.dimension = dimension
        self.logger = get_logger()

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        self.logger.info("Creating local embeddings for %s chunks", len(texts))
        return [self._embed(text) for text in texts]

    def _embed(self, text: str) -> list[float]:
        if not text or not text.strip():
            raise EmbeddingError("Cannot embed empty text.")
        vector = [0.0] * self.dimension
        tokens = _TOKEN.findall(text.lower())
        if not tokens:
            tokens = ["empty"]
        grams = list(tokens)
        grams.extend(f"{left}_{right}" for left, right in zip(tokens, tokens[1:]))
        for gram in grams:
            digest = hashlib.sha256(gram.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % self.dimension
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[index] += sign
        return _l2_normalize(vector)


class OpenAIEmbeddingProvider:
    """OpenAI embeddings adapter. The SDK is imported only when this provider is used."""

    def __init__(self, api_key: str, model: str = "text-embedding-3-small", dimension: int = 1536) -> None:
        if not api_key:
            raise EmbeddingError("OPENAI_API_KEY is required for OpenAI embeddings.")
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise EmbeddingError(
                "OpenAI SDK is unavailable. Install dependencies with pip install -r requirements.txt."
            ) from exc
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.dimension = dimension
        self.logger = get_logger()

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        if any(not text.strip() for text in texts):
            raise EmbeddingError("Cannot embed empty text.")
        self.logger.info("Requesting OpenAI embeddings for %s texts", len(texts))
        try:
            response = self.client.embeddings.create(model=self.model, input=texts)
            ordered = sorted(response.data, key=lambda item: item.index)
            return [list(item.embedding) for item in ordered]
        except EmbeddingError:
            raise
        except Exception as exc:
            raise EmbeddingError("Embedding provider failed. Please try again later.") from exc


def _l2_normalize(vector: list[float]) -> list[float]:
    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0:
        return vector
    return [value / norm for value in vector]
