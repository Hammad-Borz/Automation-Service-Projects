"""Validate RAG answers before they are returned to callers."""

from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from .exceptions import ResultValidationError
from .logger import get_logger
from .models import RAGResponse, RetrievedChunk, SourceCitation


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


def validate_rag_response(value: RAGResponse | dict[str, Any]) -> RAGResponse:
    try:
        response = RAGResponse.model_validate(value)
    except ValidationError as exc:
        get_logger().warning("RAG response validation failure: %s", exc)
        raise ResultValidationError(f"Invalid RAG result: {exc}") from exc
    if response.grounded and not response.retrieved_chunk_ids:
        raise ResultValidationError("Grounded answers must reference retrieved chunks.")
    return response
