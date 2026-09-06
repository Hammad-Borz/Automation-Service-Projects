"""Retrieval-augmented generation pipeline."""

from __future__ import annotations

from pydantic import ValidationError

from .conversation_manager import ConversationManager
from .exceptions import EmptyQueryError
from .llm_client import LLMClient, build_context
from .logger import get_logger
from .models import QueryRequest, RAGResponse
from .result_validator import citations_from_chunks, validate_rag_response
from .retriever import Retriever


class RAGPipeline:
    def __init__(
        self,
        retriever: Retriever,
        llm: LLMClient,
        conversation: ConversationManager | None = None,
        default_top_k: int = 4,
    ) -> None:
        self.retriever = retriever
        self.llm = llm
        self.conversation = conversation or ConversationManager()
        self.default_top_k = default_top_k
        self.logger = get_logger()

    def ask(self, question: str, top_k: int | None = None) -> RAGResponse:
        try:
            request = QueryRequest(question=question, top_k=top_k or self.default_top_k)
        except ValidationError as exc:
            raise EmptyQueryError("Question must not be empty.") from exc

        self.logger.info("Starting RAG query")
        retrieval_query = self.conversation.expand_query(request.question)
        chunks = self.retriever.retrieve(retrieval_query, top_k=request.top_k)
        history = self.conversation.history()
        answer, grounded = self.llm.generate(request.question, chunks, history)
        if not chunks:
            grounded = False
        sources = citations_from_chunks(chunks)
        response = validate_rag_response(
            {
                "question": request.question,
                "answer": answer,
                "grounded": grounded and bool(sources),
                "sources": sources,
                "retrieved_chunk_ids": [item.chunk.chunk_id for item in chunks],
            }
        )
        self.conversation.add_user(request.question)
        self.conversation.add_assistant(response.answer, response.sources)
        self.logger.info("Completed RAG query with %s sources", len(response.sources))
        return response

    def describe_context(self, question: str, top_k: int | None = None) -> str:
        request = QueryRequest(question=question, top_k=top_k or self.default_top_k)
        chunks = self.retriever.retrieve(
            self.conversation.expand_query(request.question),
            top_k=request.top_k,
        )
        return build_context(chunks)
