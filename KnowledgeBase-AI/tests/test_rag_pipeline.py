from pathlib import Path
from typing import Sequence

import pytest

from src.chunker import Chunker
from src.conversation_manager import ConversationManager
from src.document_processor import DocumentProcessor
from src.document_reader import DocumentReader
from src.embeddings import HashingEmbeddingProvider
from src.exceptions import EmptyKnowledgeBaseError, EmptyQueryError
from src.knowledge_base import KnowledgeBase
from src.llm_client import DemoLLMClient, INSUFFICIENT_ANSWER
from src.main import write_simple_pdf
from src.models import ConversationMessage, RetrievedChunk
from src.rag_pipeline import RAGPipeline
from src.retriever import Retriever
from src.vector_store import JsonVectorStore


class ScriptedLLM:
    def __init__(self, answer: str, grounded: bool) -> None:
        self.answer = answer
        self.grounded = grounded
        self.seen_history: list[ConversationMessage] = []

    def generate(
        self,
        question: str,
        chunks: Sequence[RetrievedChunk],
        history: Sequence[ConversationMessage],
    ) -> tuple[str, bool]:
        self.seen_history = list(history)
        if not chunks:
            return INSUFFICIENT_ANSWER, False
        return self.answer, self.grounded


def _pipeline(tmp_path: Path, llm=None) -> tuple[KnowledgeBase, RAGPipeline]:
    embeddings = HashingEmbeddingProvider(dimension=64)
    store = JsonVectorStore(tmp_path / "index.json")
    knowledge_base = KnowledgeBase(
        reader=DocumentReader(),
        processor=DocumentProcessor(),
        chunker=Chunker(chunk_size=200, chunk_overlap=40),
        embeddings=embeddings,
        store=store,
    )
    pipeline = RAGPipeline(
        retriever=Retriever(embeddings, store),
        llm=llm or DemoLLMClient(),
        conversation=ConversationManager(),
        default_top_k=3,
    )
    return knowledge_base, pipeline


def test_pipeline_returns_grounded_answer_with_citations(tmp_path: Path) -> None:
    knowledge_base, pipeline = _pipeline(
        tmp_path,
        ScriptedLLM("Employees receive 20 days of paid time off.", True),
    )
    pdf = tmp_path / "handbook.pdf"
    write_simple_pdf(pdf, "Employees receive 20 days of paid time off each calendar year.")
    knowledge_base.add_document(pdf)
    response = pipeline.ask("How many paid time off days do employees receive?")
    assert response.grounded is True
    assert "20 days" in response.answer
    assert response.sources
    assert response.sources[0].document_name == "handbook.pdf"
    assert response.sources[0].chunk_id
    assert response.retrieved_chunk_ids


def test_pipeline_says_when_context_is_insufficient(tmp_path: Path) -> None:
    knowledge_base, pipeline = _pipeline(tmp_path, DemoLLMClient())
    pdf = tmp_path / "handbook.pdf"
    write_simple_pdf(pdf, "The office kitchen has coffee and tea available all day.")
    knowledge_base.add_document(pdf)
    response = pipeline.ask("What is the company's current stock price?")
    assert response.grounded is False
    assert "do not contain enough information" in response.answer.lower()


def test_follow_up_includes_conversation_history(tmp_path: Path) -> None:
    llm = ScriptedLLM("Remote work is allowed two days each week.", True)
    knowledge_base, pipeline = _pipeline(tmp_path, llm)
    pdf = tmp_path / "handbook.pdf"
    write_simple_pdf(
        pdf,
        "Employees receive 20 days of PTO. Remote work is allowed two days each week.",
    )
    knowledge_base.add_document(pdf)
    pipeline.ask("How many PTO days do employees receive?")
    pipeline.ask("What about remote work?")
    assert llm.seen_history
    assert llm.seen_history[0].content == "How many PTO days do employees receive?"


def test_empty_question_and_empty_index(tmp_path: Path) -> None:
    knowledge_base, pipeline = _pipeline(tmp_path)
    with pytest.raises(EmptyKnowledgeBaseError):
        pipeline.ask("What is the remote work policy?")
    pdf = tmp_path / "handbook.pdf"
    write_simple_pdf(pdf, "Remote work is allowed two days each week.")
    knowledge_base.add_document(pdf)
    with pytest.raises(EmptyQueryError):
        pipeline.ask("   ")
