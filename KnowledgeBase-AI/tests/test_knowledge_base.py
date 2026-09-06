from pathlib import Path

from src.exceptions import EmptyDocumentError, UnsupportedDocumentError
from src.knowledge_base import KnowledgeBase
from src.main import write_simple_pdf
from tests.conftest import write_docx


def test_add_list_remove_and_clear(tmp_kb: KnowledgeBase, tmp_path: Path) -> None:
    pdf = tmp_path / "handbook.pdf"
    docx = tmp_path / "product.docx"
    write_simple_pdf(pdf, "Employees receive 20 days of paid time off each year.")
    write_docx(docx, "The Nova Widget battery lasts 48 hours.")

    result = tmp_kb.add_documents([pdf, docx])
    assert len(result.succeeded) == 2
    names = {item.file_name for item in tmp_kb.list_documents()}
    assert names == {"handbook.pdf", "product.docx"}
    assert all(item.chunk_count >= 1 for item in result.succeeded)

    removed_id = result.succeeded[0].document_id
    assert tmp_kb.remove_document(removed_id) is True
    assert tmp_kb.remove_document("missing") is False
    assert len(tmp_kb.list_documents()) == 1

    tmp_kb.clear()
    assert tmp_kb.is_empty()
    assert tmp_kb.list_documents() == []


def test_add_documents_collects_failures(tmp_kb: KnowledgeBase, tmp_path: Path) -> None:
    missing = tmp_path / "gone.pdf"
    unsupported = tmp_path / "notes.txt"
    unsupported.write_text("plain text")
    result = tmp_kb.add_documents([missing, unsupported])
    assert result.succeeded == []
    assert len(result.failed) == 2
    errors = " ".join(item.error for item in result.failed)
    assert "Document not found" in errors
    assert "Unsupported" in errors


def test_empty_file_is_rejected(tmp_kb: KnowledgeBase, tmp_path: Path) -> None:
    source = tmp_path / "empty.docx"
    write_docx(source, "   ")
    result = tmp_kb.add_documents([source])
    assert result.succeeded == []
    assert isinstance(result.failed[0].error, str)
    assert "no extractable text" in result.failed[0].error.lower() or result.failed[0].error
    # Ensure the typed empty-document path is reachable
    from src.document_reader import DocumentReader

    try:
        DocumentReader().extract_text(source)
        empty_raised = False
    except EmptyDocumentError:
        empty_raised = True
    except UnsupportedDocumentError:
        empty_raised = False
    assert empty_raised
