"""Application error types with user-facing messages."""


class KnowledgeBaseError(Exception):
    """Base error for recoverable application failures."""


class ConfigurationError(KnowledgeBaseError):
    """Raised when environment or runtime settings are invalid."""


class UnsupportedDocumentError(KnowledgeBaseError):
    """Raised when a file type is not supported."""


class EmptyDocumentError(KnowledgeBaseError):
    """Raised when extraction produces no meaningful text."""


class DocumentReaderError(KnowledgeBaseError):
    """Raised when a document cannot be read safely."""


class EmptyQueryError(KnowledgeBaseError):
    """Raised when a user question is blank."""


class EmptyKnowledgeBaseError(KnowledgeBaseError):
    """Raised when retrieval is requested before any documents are indexed."""


class EmbeddingError(KnowledgeBaseError):
    """Raised when embedding generation fails."""


class VectorStoreError(KnowledgeBaseError):
    """Raised when the vector store cannot complete an operation."""


class LLMError(KnowledgeBaseError):
    """Raised when the language-model provider fails."""


class ResultValidationError(KnowledgeBaseError):
    """Raised when a RAG result does not match the required contract."""
