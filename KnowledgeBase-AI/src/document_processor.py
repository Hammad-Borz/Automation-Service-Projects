"""Normalize extracted document text before chunking."""

from __future__ import annotations

import re

from .models import ExtractedDocument, PageText

_WHITESPACE = re.compile(r"[ \t]+")
_NEWLINES = re.compile(r"\n{3,}")
_NULL = re.compile(r"\x00")


def clean_text(text: str) -> str:
    """Collapse noisy whitespace without destroying paragraph structure."""
    cleaned = _NULL.sub("", text)
    cleaned = cleaned.replace("\r\n", "\n").replace("\r", "\n")
    cleaned = _WHITESPACE.sub(" ", cleaned)
    cleaned = _NEWLINES.sub("\n\n", cleaned)
    return cleaned.strip()


class DocumentProcessor:
    """Prepare extracted documents for indexing."""

    def process(self, document: ExtractedDocument) -> ExtractedDocument:
        pages = [
            PageText(page_number=page.page_number, text=clean_text(page.text))
            for page in document.pages
            if clean_text(page.text)
        ]
        text = clean_text(document.text)
        return ExtractedDocument(metadata=document.metadata, text=text, pages=pages)
