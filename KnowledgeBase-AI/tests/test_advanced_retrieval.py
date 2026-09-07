from pathlib import Path

from src.embeddings import HashingEmbeddingProvider
from src.hybrid_retriever import reciprocal_rank_fusion
from src.keyword_retriever import BM25Retriever
from src.models import DocumentChunk, DocumentMetadata, RetrievedChunk
from src.reranker import LexicalReranker
from src.result_validator import supporting_chunks
from src.retriever import Retriever
from src.vector_store import JsonVectorStore


def _chunk(document_id: str, name: str, text: str, page: int | None = None) -> DocumentChunk:
    return DocumentChunk(
        document_id=document_id,
        document_name=name,
        file_type="pdf",
        text=text,
        chunk_index=0,
        page_number=page,
    )


def _index(store: JsonVectorStore, embeddings: HashingEmbeddingProvider, chunk: DocumentChunk) -> None:
    store.upsert(
        DocumentMetadata(
            document_id=chunk.document_id,
            file_name=chunk.document_name,
            file_type=chunk.file_type,
            source_path=chunk.document_name,
        ),
        [chunk],
        embeddings.embed_documents([chunk.text]),
    )


def test_bm25_produces_an_independent_keyword_ranking() -> None:
    chunks = [
        _chunk("doc_a", "a.pdf", "refund approval threshold policy"),
        _chunk("doc_b", "b.pdf", "holiday calendar and office closures"),
    ]
    results = BM25Retriever(chunks).retrieve("refund approval", top_k=2)
    assert results
    assert results[0].chunk.document_id == "doc_a"


def test_rrf_combines_rankings_deterministically() -> None:
    first = _chunk("doc_a", "a.pdf", "alpha")
    second = _chunk("doc_b", "b.pdf", "beta")
    fused = reciprocal_rank_fusion(
        [[RetrievedChunk(chunk=first, score=0.9)], [RetrievedChunk(chunk=second, score=0.9)]],
        top_k=2,
    )
    assert [item.chunk.document_id for item in fused] == ["doc_a", "doc_b"]
    assert fused[0].score == fused[1].score


def test_reranker_changes_scores_using_query_coverage() -> None:
    weak = _chunk("doc_a", "a.pdf", "policy document")
    strong = _chunk("doc_b", "b.pdf", "refund approval requires manager approval")
    results = LexicalReranker().rerank(
        "refund approval",
        [
            RetrievedChunk(chunk=weak, score=1.0),
            RetrievedChunk(chunk=strong, score=0.1),
        ],
        top_k=2,
    )
    assert results[0].chunk.document_id == "doc_b"
    assert results[0].score > 0.1


def test_metadata_filter_limits_both_retrieval_strategies(tmp_path: Path) -> None:
    embeddings = HashingEmbeddingProvider(dimension=64)
    store = JsonVectorStore(tmp_path / "index.json")
    _index(store, embeddings, _chunk("doc_a", "handbook.pdf", "refund approval is required", page=2))
    _index(store, embeddings, _chunk("doc_b", "guide.docx", "refund approval is required", page=4))
    results = Retriever(embeddings, store, minimum_relevance=0.0).retrieve(
        "refund approval", top_k=4, filters={"file_name": "guide.docx"}
    )
    assert results
    assert {item.chunk.document_name for item in results} == {"guide.docx"}


def test_weak_retrieval_is_abstained_from(tmp_path: Path) -> None:
    embeddings = HashingEmbeddingProvider(dimension=64)
    store = JsonVectorStore(tmp_path / "index.json")
    _index(store, embeddings, _chunk("doc_a", "office.pdf", "coffee and tea are available"))
    results = Retriever(embeddings, store, minimum_relevance=0.5).retrieve(
        "quantum satellite propulsion", top_k=4
    )
    assert results == []


def test_citation_selection_excludes_irrelevant_retrieved_chunks() -> None:
    relevant = _chunk("doc_a", "handbook.pdf", "employees receive 20 days of paid time off")
    irrelevant = _chunk("doc_b", "guide.docx", "the widget battery lasts 48 hours")
    selected = supporting_chunks(
        "Employees receive 20 days of paid time off.",
        [
            RetrievedChunk(chunk=relevant, score=0.9),
            RetrievedChunk(chunk=irrelevant, score=0.4),
        ],
    )
    assert [item.chunk.document_id for item in selected] == ["doc_a"]
