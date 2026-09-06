from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.document_reader import DocumentReader
from src.exceptions import DocumentReaderError, EmptyDocumentError, UnsupportedDocumentError
from src.main import write_simple_pdf
from tests.conftest import write_docx


def test_extracts_pdf_text(tmp_path: Path) -> None:
    source = tmp_path / "handbook.pdf"
    write_simple_pdf(source, "Remote work is allowed two days each week.")
    text = DocumentReader().extract_text(source)
    assert "Remote work is allowed two days each week." in text


def test_extracts_docx_text(tmp_path: Path) -> None:
    source = write_docx(tmp_path / "guide.docx", "The battery lasts 48 hours.")
    assert "The battery lasts 48 hours." in DocumentReader().extract_text(source)


def test_pdf_preserves_page_numbers(tmp_path: Path) -> None:
    source = tmp_path / "paged.pdf"
    write_simple_pdf(source, "Page one content")
    extracted = DocumentReader().read(source)
    assert extracted.pages[0].page_number == 1
    assert extracted.metadata.file_name == "paged.pdf"
    assert extracted.metadata.file_type == "pdf"


def test_rejects_unsupported_document(tmp_path: Path) -> None:
    source = tmp_path / "notes.txt"
    source.write_text("notes")
    with pytest.raises(UnsupportedDocumentError, match="Supported types"):
        DocumentReader().extract_text(source)


def test_rejects_missing_document(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="Document not found"):
        DocumentReader().extract_text(tmp_path / "missing.pdf")


@patch("src.document_reader.PdfReader")
def test_rejects_empty_document(mock_reader: MagicMock, tmp_path: Path) -> None:
    source = tmp_path / "empty.pdf"
    source.touch()
    page = MagicMock()
    page.extract_text.return_value = None
    mock_reader.return_value.pages = [page]
    with pytest.raises(EmptyDocumentError):
        DocumentReader().extract_text(source)


@patch("src.document_reader.PdfReader", side_effect=OSError("broken"))
def test_rejects_unreadable_document(_mock_reader: MagicMock, tmp_path: Path) -> None:
    source = tmp_path / "corrupt.pdf"
    source.write_bytes(b"not a pdf")
    with pytest.raises(DocumentReaderError, match="Could not read document"):
        DocumentReader().extract_text(source)
