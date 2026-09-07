"""Validate RAG answers before they are returned to callers."""

from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from .exceptions import ResultValidationError
from .logger import get_logger
from .models import RAGResponse, RetrievedChunk, SourceCitation
from .keyword_retriever import tokenize


def citations_from_chunks(chunks: list[RetrievedChunk]) -> list[SourceCitation]:
    citations: list[SourceCitation] = []
    seen: set[str] = set()
    for retrieved in chunks:
        chunk = retrieved.chunk
        if chunk.chunk_id in seen:
            continue
        seen.add(chunk.chunk_id)
        citations.append(
            SourceCitation(
                document_id=chunk.document_id,
                document_name=chunk.document_name,
                chunk_id=chunk.chunk_id,
                page_number=chunk.page_number,
                score=retrieved.score,
            )
        )
    return citations


def supporting_chunks(answer: str, chunks: list[RetrievedChunk]) -> list[RetrievedChunk]:
    """Select chunks with deterministic lexical evidence in the final answer."""
    answer_tokens = _meaningful_tokens(answer)
    selected: list[RetrievedChunk] = []
    for retrieved in chunks:
        chunk_tokens = _meaningful_tokens(retrieved.chunk.text)
        if len(answer_tokens.intersection(chunk_tokens)) >= 2:
            selected.append(retrieved)
    return selected


_CITATION_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "in",
    "is", "it", "of", "on", "or", "that", "the", "this", "to", "was", "with",
}


def _meaningful_tokens(text: str) -> set[str]:
    return {token for token in tokenize(text) if token not in _CITATION_STOPWORDS}


def validate_rag_response(value: RAGResponse | dict[str, Any]) -> RAGResponse:
    try:
        response = RAGResponse.model_validate(value)
    except ValidationError as exc:
        get_logger().warning("RAG response validation failure: %s", exc)
        raise ResultValidationError(f"Invalid RAG result: {exc}") from exc
    if response.grounded and not response.retrieved_chunk_ids:
        raise ResultValidationError("Grounded answers must reference retrieved chunks.")
    return response
