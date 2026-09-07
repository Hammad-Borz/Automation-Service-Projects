"""Lexical retrieval using a small, dependency-free BM25 implementation."""

from __future__ import annotations

import math
import re
from collections import Counter
from typing import Iterable

from .models import DocumentChunk, RetrievedChunk

_TOKEN = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    return _TOKEN.findall(text.lower())


class BM25Retriever:
    """Rank indexed chunks independently from vector retrieval."""

    def __init__(self, chunks: Iterable[DocumentChunk], k1: float = 1.5, b: float = 0.75) -> None:
        self.chunks = list(chunks)
        self.k1 = k1
        self.b = b
        self._tokens = [tokenize(chunk.text) for chunk in self.chunks]
        self._frequencies = [Counter(tokens) for tokens in self._tokens]
        self._average_length = (
            sum(len(tokens) for tokens in self._tokens) / len(self._tokens)
            if self._tokens
            else 0.0
        )
        self._document_frequency: Counter[str] = Counter()
        for tokens in self._tokens:
            self._document_frequency.update(set(tokens))

    def retrieve(
        self,
        query: str,
        top_k: int = 10,
        filters: dict[str, object] | None = None,
    ) -> list[RetrievedChunk]:
        query_tokens = tokenize(query)
        scored: list[tuple[float, DocumentChunk]] = []
        total_documents = len(self.chunks)
        for chunk, tokens, frequencies in zip(self.chunks, self._tokens, self._frequencies):
            if not _matches_filters(chunk, filters):
                continue
            length = len(tokens)
            score = 0.0
            for term in query_tokens:
                term_frequency = frequencies.get(term, 0)
                if not term_frequency:
                    continue
                document_frequency = self._document_frequency[term]
                idf = math.log(1 + (total_documents - document_frequency + 0.5) / (document_frequency + 0.5))
                denominator = term_frequency + self.k1 * (
                    1 - self.b + self.b * length / (self._average_length or 1.0)
                )
                score += idf * (term_frequency * (self.k1 + 1)) / denominator
            if score > 0:
                scored.append((score, chunk))
        scored.sort(key=lambda item: (-item[0], item[1].chunk_id))
        return [RetrievedChunk(chunk=chunk, score=_normalize_bm25(score)) for score, chunk in scored[:top_k]]


def _normalize_bm25(score: float) -> float:
    return score / (score + 1.0)


def _matches_filters(chunk: DocumentChunk, filters: dict[str, object] | None) -> bool:
    if not filters:
        return True
    checks = {
        "document_id": chunk.document_id,
        "document_name": chunk.document_name,
        "file_name": chunk.document_name,
        "file_type": chunk.file_type,
        "page_number": chunk.page_number,
    }
    return all(checks.get(key) == value for key, value in filters.items() if key in checks)