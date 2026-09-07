"""Rank-fusion utilities for independent semantic and lexical retrieval."""

from __future__ import annotations

from typing import Sequence

from .models import RetrievedChunk


def reciprocal_rank_fusion(
    rankings: Sequence[Sequence[RetrievedChunk]],
    top_k: int,
    k: int = 60,
) -> list[RetrievedChunk]:
    """Combine independent rankings with deterministic reciprocal-rank fusion."""
    fused: dict[str, tuple[RetrievedChunk, float]] = {}
    for ranking in rankings:
        for rank, item in enumerate(ranking, start=1):
            contribution = 1.0 / (k + rank)
            current = fused.get(item.chunk.chunk_id)
            if current:
                fused[item.chunk.chunk_id] = (current[0], current[1] + contribution)
            else:
                fused[item.chunk.chunk_id] = (item, contribution)
    if not fused:
        return []
    maximum = max(score for _, score in fused.values())
    ordered = sorted(
        fused.values(),
        key=lambda item: (
            -round(item[1], 12),
            item[0].chunk.document_id,
            item[0].chunk.chunk_id,
        ),
    )
    return [item.model_copy(update={"score": score / maximum}) for item, score in ordered[:top_k]]