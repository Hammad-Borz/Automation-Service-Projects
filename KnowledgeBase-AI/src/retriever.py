"""Query embedding and nearest-chunk retrieval."""

from __future__ import annotations

from .embeddings import EmbeddingProvider
from .exceptions import EmptyKnowledgeBaseError, EmptyQueryError
from .logger import get_logger
from .models import RetrievedChunk
from .vector_store import VectorStore


class Retriever:
    def __init__(self, embeddings: EmbeddingProvider, store: VectorStore) -> None:
        self.embeddings = embeddings
        self.store = store
        self.logger = get_logger()

    def retrieve(self, question: str, top_k: int = 4) -> list[RetrievedChunk]:
        cleaned = question.strip()
        if not cleaned:
            raise EmptyQueryError("Question must not be empty.")
        if self.store.is_empty():
            raise EmptyKnowledgeBaseError(
                "No documents have been indexed yet. Add documents before asking questions."
            )
        self.logger.info("Retrieving context for a user question")
        query_embedding = self.embeddings.embed_query(cleaned)
        return self.store.search(query_embedding, top_k=top_k)
