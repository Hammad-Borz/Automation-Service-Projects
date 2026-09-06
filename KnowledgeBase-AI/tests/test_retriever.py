from pathlib import Path

import pytest

from src.embeddings import HashingEmbeddingProvider
from src.exceptions import EmptyKnowledgeBaseError, EmptyQueryError
from src.models import DocumentChunk, DocumentMetadata
from src.retriever import Retriever
from src.vector_store import JsonVectorStore


def _index(store: JsonVectorStore, embeddings: HashingEmbeddingProvider, text: str, name: str) -> None:
    chunk = DocumentChunk(
        document_id=f"doc_{name}",
        document_name=name,
        file_type="pdf",
        text=text,
        chunk_index=0,
    )
    metadata = DocumentMetadata(
        document_id=chunk.document_id,
        file_name=name,
        file_type="pdf",
        source_path=name,
        chunk_count=1,
    )
    store.upsert(metadata, [chunk], embeddings.embed_documents([text]))


def test_retrieves_the_most_relevant_chunk(tmp_path: Path) -> None:
    embeddings = HashingEmbeddingProvider(dimension=64)
    store = JsonVectorStore(tmp_path / "index.json")
    _index(store, embeddings, "Employees receive 20 days of paid time off each year.", "pto.pdf")
    _index(store, embeddings, "The office kitchen has coffee and tea available.", "office.pdf")
    retriever = Retriever(embeddings, store)
    results = retriever.retrieve("How many paid time off days do employees receive?", top_k=1)
    assert results
    assert results[0].chunk.document_name == "pto.pdf"
    assert 0.0 <= results[0].score <= 1.0


def test_empty_knowledge_base_raises(tmp_path: Path) -> None:
    retriever = Retriever(HashingEmbeddingProvider(dimension=64), JsonVectorStore(tmp_path / "index.json"))
    with pytest.raises(EmptyKnowledgeBaseError, match="No documents have been indexed"):
        retriever.retrieve("What is the remote work policy?")


def test_empty_question_raises(tmp_path: Path) -> None:
    embeddings = HashingEmbeddingProvider(dimension=64)
    store = JsonVectorStore(tmp_path / "index.json")
    _index(store, embeddings, "Policy text lives here.", "policy.pdf")
    with pytest.raises(EmptyQueryError):
        Retriever(embeddings, store).retrieve("   ")
