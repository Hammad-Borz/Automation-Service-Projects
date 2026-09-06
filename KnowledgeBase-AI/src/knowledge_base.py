"""Document catalog and indexing facade over the RAG storage layer."""

from __future__ import annotations

from pathlib import Path

from .chunker import Chunker
from .document_processor import DocumentProcessor
from .document_reader import DocumentReader
from .embeddings import EmbeddingProvider
from .exceptions import KnowledgeBaseError
from .logger import get_logger
from .models import DocumentMetadata, IngestFailure, IngestResult
from .vector_store import VectorStore


class KnowledgeBase:
    def __init__(
        self,
        reader: DocumentReader,
        processor: DocumentProcessor,
        chunker: Chunker,
        embeddings: EmbeddingProvider,
        store: VectorStore,
    ) -> None:
        self.reader = reader
        self.processor = processor
        self.chunker = chunker
        self.embeddings = embeddings
        self.store = store
        self.logger = get_logger()

    def add_document(self, path: str | Path) -> DocumentMetadata:
        source = Path(path)
        self.logger.info("Ingesting document %s", source.name)
        extracted = self.reader.read(source)
        processed = self.processor.process(extracted)
        chunks = self.chunker.chunk(processed)
        self.logger.info("Created %s chunks for %s", len(chunks), source.name)
        vectors = self.embeddings.embed_documents([chunk.text for chunk in chunks])
        metadata = processed.metadata.model_copy(update={"chunk_count": len(chunks)})
        self.store.upsert(metadata, chunks, vectors)
        return metadata

    def add_documents(self, paths: list[str | Path]) -> IngestResult:
        result = IngestResult()
        for path in paths:
            try:
                result.succeeded.append(self.add_document(path))
            except (KnowledgeBaseError, FileNotFoundError, OSError) as exc:
                self.logger.error("Failed to ingest %s: %s", path, exc)
                result.failed.append(IngestFailure(path=str(path), error=str(exc)))
        return result

    def list_documents(self) -> list[DocumentMetadata]:
        return self.store.list_documents()

    def remove_document(self, document_id: str) -> bool:
        return self.store.delete_document(document_id)

    def clear(self) -> None:
        self.store.clear()

    def is_empty(self) -> bool:
        return self.store.is_empty()
