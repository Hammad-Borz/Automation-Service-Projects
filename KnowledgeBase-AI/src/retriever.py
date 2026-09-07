"""Query embedding and nearest-chunk retrieval."""

from __future__ import annotations

from .embeddings import EmbeddingProvider
from .exceptions import EmptyKnowledgeBaseError, EmptyQueryError
from .hybrid_retriever import reciprocal_rank_fusion
from .keyword_retriever import BM25Retriever
from .logger import get_logger
from .models import RetrievedChunk
from .reranker import LexicalReranker
from .vector_store import VectorStore


class Retriever:
    def __init__(
        self,
        embeddings: EmbeddingProvider,
        store: VectorStore,
        candidate_k: int = 12,
        minimum_relevance: float = 0.35,
        rrf_k: int = 60,
    ) -> None:
        self.embeddings = embeddings
        self.store = store
        self.candidate_k = candidate_k
        self.minimum_relevance = minimum_relevance
        self.rrf_k = rrf_k
        self.reranker = LexicalReranker()
        self.logger = get_logger()

    def retrieve(
        self,
        question: str,
        top_k: int = 4,
        filters: dict[str, object] | None = None,
    ) -> list[RetrievedChunk]:
        cleaned = question.strip()
        if not cleaned:
            raise EmptyQueryError("Question must not be empty.")
        if self.store.is_empty():
            raise EmptyKnowledgeBaseError(
                "No documents have been indexed yet. Add documents before asking questions."
            )
        self.logger.info("Retrieving context for a user question")
        query_embedding = self.embeddings.embed_query(cleaned)
        candidate_k = max(top_k, self.candidate_k)
        semantic = self.store.search(query_embedding, top_k=candidate_k, filters=filters)
        lexical = BM25Retriever(self.store.chunks(filters)).retrieve(
            cleaned, top_k=candidate_k, filters=filters
        )
        fused = reciprocal_rank_fusion([semantic, lexical], top_k=candidate_k, k=self.rrf_k)
        reranked = self.reranker.rerank(cleaned, fused, top_k=top_k)
        return [item for item in reranked if item.score >= self.minimum_relevance]
