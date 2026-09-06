"""Configurable document chunking with source metadata preservation."""

from __future__ import annotations

import re

from .models import DocumentChunk, ExtractedDocument, PageText, new_id

_WORD = re.compile(r"\S+")


class Chunker:
    """Split document text into overlapping character windows on word boundaries."""

    def __init__(self, chunk_size: int = 400, chunk_overlap: int = 80) -> None:
        if chunk_size < 50:
            raise ValueError("chunk_size must be at least 50")
        if chunk_overlap < 0 or chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be >= 0 and smaller than chunk_size")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, document: ExtractedDocument) -> list[DocumentChunk]:
        segments = document.pages or [PageText(page_number=None, text=document.text)]

        chunks: list[DocumentChunk] = []
        index = 0
        for segment in segments:
            for text in self._split_text(segment.text):
                chunks.append(
                    DocumentChunk(
                        chunk_id=new_id("chunk"),
                        document_id=document.metadata.document_id,
                        document_name=document.metadata.file_name,
                        file_type=document.metadata.file_type,
                        text=text,
                        chunk_index=index,
                        page_number=segment.page_number,
                    )
                )
                index += 1
        return chunks

    def _split_text(self, text: str) -> list[str]:
        text = text.strip()
        if not text:
            return []
        if len(text) <= self.chunk_size:
            return [text]

        words = list(_WORD.finditer(text))
        pieces: list[str] = []
        start = 0
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            if end < len(text):
                boundary = self._last_word_end(words, start, end)
                if boundary is not None and boundary > start:
                    end = boundary
            piece = text[start:end].strip()
            if piece:
                pieces.append(piece)
            if end >= len(text):
                break
            start = max(end - self.chunk_overlap, start + 1)
        return pieces

    @staticmethod
    def _last_word_end(words: list[re.Match[str]], start: int, end: int) -> int | None:
        last = None
        for match in words:
            if match.start() < start:
                continue
            if match.end() <= end:
                last = match.end()
            else:
                break
        return last
