"""Text extraction for supported document formats."""

from pathlib import Path

from docx import Document
from pypdf import PdfReader


class DocumentReaderError(Exception):
    """Base error for document reading failures."""


class UnsupportedDocumentError(DocumentReaderError):
    """Raised when a file type is not supported."""


class EmptyDocumentError(DocumentReaderError):
    """Raised when extraction produces no meaningful text."""


class DocumentReader:
    """Extract text from PDF and DOCX documents only."""

    supported_extensions = {".pdf", ".docx"}

    def extract_text(self, document_path: str | Path) -> str:
        path = Path(document_path)
        if not path.is_file():
            raise FileNotFoundError(f"Document not found: {path}")
        if path.suffix.lower() not in self.supported_extensions:
            raise UnsupportedDocumentError(
                f"Unsupported document type '{path.suffix}'. Supported types: PDF, DOCX."
            )

        try:
            text = self._read_pdf(path) if path.suffix.lower() == ".pdf" else self._read_docx(path)
        except DocumentReaderError:
            raise
        except Exception as exc:
            raise DocumentReaderError(f"Could not read document '{path.name}'.") from exc

        text = text.strip()
        if not text:
            raise EmptyDocumentError(f"Document '{path.name}' contains no extractable text.")
        return text

    @staticmethod
    def _read_pdf(path: Path) -> str:
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    @staticmethod
    def _read_docx(path: Path) -> str:
        document = Document(str(path))
        return "\n".join(paragraph.text for paragraph in document.paragraphs)
