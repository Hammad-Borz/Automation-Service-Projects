import pytest

from src.exceptions import ResultValidationError
from src.models import DocumentChunk, RetrievedChunk
from src.result_validator import citations_from_chunks, validate_rag_response


def test_citations_include_document_and_chunk_identifiers() -> None:
    retrieved = RetrievedChunk(
        chunk=DocumentChunk(
            chunk_id="chunk_abc",
            document_id="doc_1",
            document_name="handbook.pdf",
            file_type="pdf",
            text="Employees receive 20 days of PTO.",
            chunk_index=0,
            page_number=3,
        ),
        score=0.91,
    )
    citations = citations_from_chunks([retrieved, retrieved])
    assert len(citations) == 1
    assert citations[0].document_name == "handbook.pdf"
    assert citations[0].chunk_id == "chunk_abc"
    assert citations[0].page_number == 3


def test_validates_complete_rag_response() -> None:
    response = validate_rag_response(
        {
            "question": "How many PTO days are provided?",
            "answer": "Employees receive 20 days of PTO.",
            "grounded": True,
            "sources": [
                {
                    "document_id": "doc_1",
                    "document_name": "handbook.pdf",
                    "chunk_id": "chunk_abc",
                    "score": 0.9,
                }
            ],
            "retrieved_chunk_ids": ["chunk_abc"],
        }
    )
    assert response.grounded is True


def test_rejects_grounded_answer_without_sources() -> None:
    with pytest.raises(ResultValidationError):
        validate_rag_response(
            {
                "question": "How many PTO days are provided?",
                "answer": "Employees receive 20 days of PTO.",
                "grounded": True,
                "sources": [],
                "retrieved_chunk_ids": ["chunk_abc"],
            }
        )


def test_rejects_blank_answer() -> None:
    with pytest.raises(ResultValidationError):
        validate_rag_response(
            {
                "question": "What is the policy?",
                "answer": "   ",
                "grounded": False,
                "sources": [],
                "retrieved_chunk_ids": [],
            }
        )


def test_rejects_grounded_answer_without_retrieved_chunks() -> None:
    with pytest.raises(ResultValidationError, match="retrieved chunks"):
        validate_rag_response(
            {
                "question": "How many PTO days are provided?",
                "answer": "Employees receive 20 days of PTO.",
                "grounded": True,
                "sources": [
                    {
                        "document_id": "doc_1",
                        "document_name": "handbook.pdf",
                        "chunk_id": "chunk_abc",
                        "score": 0.9,
                    }
                ],
                "retrieved_chunk_ids": [],
            }
        )
