"""Local JSON vector store with a replaceable persistence interface."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Protocol

from .exceptions import VectorStoreError
from .logger import get_logger
from .models import DocumentChunk, DocumentMetadata, RetrievedChunk


class VectorStore(Protocol):
    def upsert(
        self,
        metadata: DocumentMetadata,
        chunks: list[DocumentChunk],
        embeddings: list[list[float]],
    ) -> None: ...

    def search(self, query_embedding: list[float], top_k: int = 4) -> list[RetrievedChunk]: ...

    def list_documents(self) -> list[DocumentMetadata]: ...

    def delete_document(self, document_id: str) -> bool: ...

    def clear(self) -> None: ...

    def is_empty(self) -> bool: ...


class JsonVectorStore:
    """Stores document metadata, chunks, and embeddings in a single JSON file."""

    def __init__(self, persist_path: str | Path | None = None) -> None:
        self.persist_path = Path(persist_path) if persist_path else None
        self.logger = get_logger()
        self._documents: dict[str, dict[str, Any]] = {}
        self._records: list[dict[str, Any]] = []
        if self.persist_path:
            self._load()

    def upsert(
        self,
        metadata: DocumentMetadata,
        chunks: list[DocumentChunk],
        embeddings: list[list[float]],
    ) -> None:
        if len(chunks) != len(embeddings):
            raise VectorStoreError("Each chunk must have exactly one embedding.")
        self.delete_document(metadata.document_id)
        payload = metadata.model_dump(mode="json")
        payload["chunk_count"] = len(chunks)
        self._documents[metadata.document_id] = payload
        for chunk, embedding in zip(chunks, embeddings):
            self._records.append(
                {
                    "chunk": chunk.model_dump(mode="json"),
                    "embedding": embedding,
                }
            )
        self.logger.info(
            "Indexed document %s with %s chunks", metadata.file_name, len(chunks)
        )
        self._save()

    def search(self, query_embedding: list[float], top_k: int = 4) -> list[RetrievedChunk]:
        if not self._records:
            return []
        try:
            scored: list[tuple[float, dict[str, Any]]] = []
            for record in self._records:
                score = cosine_similarity(query_embedding, record["embedding"])
                scored.append((max(0.0, min(1.0, score)), record))
            scored.sort(key=lambda item: item[0], reverse=True)
            results: list[RetrievedChunk] = []
            for score, record in scored[:top_k]:
                if score <= 0:
                    continue
                results.append(
                    RetrievedChunk(chunk=DocumentChunk.model_validate(record["chunk"]), score=score)
                )
            self.logger.info("Retrieved %s chunks", len(results))
            return results
        except VectorStoreError:
            raise
        except Exception as exc:
            raise VectorStoreError("Vector store search failed.") from exc

    def list_documents(self) -> list[DocumentMetadata]:
        return [DocumentMetadata.model_validate(item) for item in self._documents.values()]

    def delete_document(self, document_id: str) -> bool:
        existed = document_id in self._documents
        self._documents.pop(document_id, None)
        self._records = [
            record for record in self._records if record["chunk"]["document_id"] != document_id
        ]
        if existed:
            self.logger.info("Removed document %s from the knowledge base", document_id)
            self._save()
        return existed

    def clear(self) -> None:
        self._documents = {}
        self._records = []
        self.logger.info("Cleared the knowledge base")
        self._save()

    def is_empty(self) -> bool:
        return not self._records

    def _load(self) -> None:
        if self.persist_path is None or not self.persist_path.exists():
            return
        try:
            payload = json.loads(self.persist_path.read_text(encoding="utf-8"))
            self._documents = payload.get("documents", {})
            self._records = payload.get("records", [])
        except Exception as exc:
            raise VectorStoreError(f"Could not load vector store from '{self.persist_path}'.") from exc

    def _save(self) -> None:
        if self.persist_path is None:
            return
        try:
            self.persist_path.parent.mkdir(parents=True, exist_ok=True)
            payload = {"documents": self._documents, "records": self._records}
            self.persist_path.write_text(json.dumps(payload), encoding="utf-8")
        except Exception as exc:
            raise VectorStoreError(f"Could not save vector store to '{self.persist_path}'.") from exc


def cosine_similarity(left: list[float], right: list[float]) -> float:
    if len(left) != len(right):
        raise VectorStoreError("Query and stored embeddings must have the same dimension.")
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot / (left_norm * right_norm)
