"""Validated domain models for the RAG pipeline."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator, model_validator


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


class DocumentMetadata(BaseModel):
    document_id: str = Field(default_factory=lambda: new_id("doc"))
    file_name: str = Field(min_length=1)
    file_type: str = Field(min_length=1)
    source_path: str = Field(min_length=1)
    page_count: int | None = Field(default=None, ge=1)
    indexed_at: datetime = Field(default_factory=utc_now)
    chunk_count: int = Field(default=0, ge=0)

    @field_validator("file_name", "file_type", "source_path")
    @classmethod
    def not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value

    @field_validator("file_type")
    @classmethod
    def normalize_type(cls, value: str) -> str:
        return value.lower().lstrip(".")


class PageText(BaseModel):
    page_number: int | None = Field(default=None, ge=1)
    text: str


class ExtractedDocument(BaseModel):
    metadata: DocumentMetadata
    text: str = Field(min_length=1)
    pages: list[PageText] = Field(default_factory=list)

    @field_validator("text")
    @classmethod
    def text_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("extracted text must not be blank")
        return value


class DocumentChunk(BaseModel):
    chunk_id: str = Field(default_factory=lambda: new_id("chunk"))
    document_id: str = Field(min_length=1)
    document_name: str = Field(min_length=1)
    file_type: str = Field(min_length=1)
    text: str = Field(min_length=1)
    chunk_index: int = Field(ge=0)
    page_number: int | None = Field(default=None, ge=1)
    char_count: int = Field(default=0, ge=0)

    @model_validator(mode="after")
    def set_char_count(self) -> "DocumentChunk":
        if self.char_count == 0:
            self.char_count = len(self.text)
        return self


class RetrievedChunk(BaseModel):
    chunk: DocumentChunk
    score: float = Field(ge=0.0, le=1.0)


class QueryRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4_000)
    top_k: int = Field(default=4, ge=1, le=20)

    @field_validator("question")
    @classmethod
    def question_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("question must not be blank")
        return value


class SourceCitation(BaseModel):
    document_id: str = Field(min_length=1)
    document_name: str = Field(min_length=1)
    chunk_id: str = Field(min_length=1)
    page_number: int | None = Field(default=None, ge=1)
    score: float = Field(ge=0.0, le=1.0)


class RAGResponse(BaseModel):
    question: str = Field(min_length=1)
    answer: str = Field(min_length=1)
    grounded: bool
    sources: list[SourceCitation] = Field(default_factory=list)
    retrieved_chunk_ids: list[str] = Field(default_factory=list)

    @field_validator("question", "answer")
    @classmethod
    def not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value

    @model_validator(mode="after")
    def grounded_requires_sources(self) -> "RAGResponse":
        if self.grounded and not self.sources:
            raise ValueError("grounded answers must include at least one source citation")
        return self


class ConversationMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1)
    sources: list[SourceCitation] = Field(default_factory=list)

    @field_validator("content")
    @classmethod
    def content_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("message content must not be blank")
        return value


class IngestFailure(BaseModel):
    path: str
    error: str


class IngestResult(BaseModel):
    succeeded: list[DocumentMetadata] = Field(default_factory=list)
    failed: list[IngestFailure] = Field(default_factory=list)
