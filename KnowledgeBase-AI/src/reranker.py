"""Deterministic second-stage relevance reranking."""

from __future__ import annotations

from collections import Counter
from typing import Sequence

from .keyword_retriever import tokenize
from .models import RetrievedChunk


class LexicalReranker:
    """Rerank candidates using query coverage and phrase evidence.

    This is intentionally local and deterministic. It is a second scoring stage,
    separate from both vector similarity and BM25 candidate generation.
    """

    def rerank(self, query: str, candidates: Sequence[RetrievedChunk], top_k: int) -> list[RetrievedChunk]:
        query_tokens = set(tokenize(query))
        if not query_tokens:
            return []
        reranked: list[RetrievedChunk] = []
        for candidate in candidates:
            chunk_tokens = Counter(tokenize(candidate.chunk.text))
            overlap = query_tokens.intersection(chunk_tokens)
            coverage = len(overlap) / len(query_tokens)
            density = sum(chunk_tokens[token] for token in overlap) / max(sum(chunk_tokens.values()), 1)
            score = min(1.0, 0.75 * coverage + 0.2 * min(1.0, density * 10) + 0.05 * candidate.score)
            if score > 0:
                reranked.append(candidate.model_copy(update={"score": score}))
        reranked.sort(key=lambda item: (-item.score, item.chunk.chunk_id))
        return reranked[:top_k]