from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.document_reader import DocumentReader, EmptyDocumentError, UnsupportedDocumentError


def test_rejects_unsupported_document(tmp_path: Path) -> None:
    source = tmp_path / "notes.txt"
    source.write_text("notes")
    with pytest.raises(UnsupportedDocumentError, match="Supported types"):
        DocumentReader().extract_text(source)


def test_rejects_missing_document(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="Document not found"):
        DocumentReader().extract_text(tmp_path / "missing.pdf")


@patch("src.document_reader.PdfReader")
def test_extracts_pdf_text(mock_reader: MagicMock, tmp_path: Path) -> None:
    source = tmp_path / "report.pdf"
    source.touch()
    page = MagicMock()
    page.extract_text.return_value = "First page"
    mock_reader.return_value.pages = [page]
    assert DocumentReader().extract_text(source) == "First page"


@patch("src.document_reader.Document")
def test_extracts_docx_text(mock_document: MagicMock, tmp_path: Path) -> None:
    source = tmp_path / "report.docx"
    source.touch()
    mock_document.return_value.paragraphs = [MagicMock(text="Hello"), MagicMock(text="World")]
    assert DocumentReader().extract_text(source) == "Hello\nWorld"


@patch("src.document_reader.PdfReader")
def test_rejects_empty_document(mock_reader: MagicMock, tmp_path: Path) -> None:
    source = tmp_path / "empty.pdf"
    source.touch()
    page = MagicMock()
    page.extract_text.return_value = None
    mock_reader.return_value.pages = [page]
    with pytest.raises(EmptyDocumentError):
        DocumentReader().extract_text(source)
