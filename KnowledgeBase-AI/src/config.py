"""Environment-backed application settings."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

from .exceptions import ConfigurationError

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SUPPORTED_MODES = {"demo", "openai"}


class Settings:
    """Runtime configuration loaded from environment variables."""

    def __init__(
        self,
        *,
        mode: str = "demo",
        openai_api_key: str | None = None,
        openai_model: str = "gpt-4o-mini",
        openai_embedding_model: str = "text-embedding-3-small",
        chunk_size: int = 400,
        chunk_overlap: int = 80,
        top_k: int = 4,
        embedding_dimension: int = 256,
        documents_dir: Path | None = None,
        vector_store_dir: Path | None = None,
        log_dir: Path | None = None,
    ) -> None:
        self.mode = mode.strip().lower()
        self.openai_api_key = openai_api_key or None
        self.openai_model = openai_model.strip()
        self.openai_embedding_model = openai_embedding_model.strip()
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.top_k = top_k
        self.embedding_dimension = embedding_dimension
        self.documents_dir = documents_dir or (PROJECT_ROOT / "data" / "documents")
        self.vector_store_dir = vector_store_dir or (PROJECT_ROOT / "data" / "vector_store")
        self.log_dir = log_dir or (PROJECT_ROOT / "logs")
        self.validate()

    def validate(self) -> None:
        if self.mode not in SUPPORTED_MODES:
            raise ConfigurationError(
                f"Invalid KNOWLEDGEBASE_MODE '{self.mode}'. Use 'demo' or 'openai'."
            )
        if self.chunk_size < 50:
            raise ConfigurationError("CHUNK_SIZE must be at least 50 characters.")
        if self.chunk_overlap < 0 or self.chunk_overlap >= self.chunk_size:
            raise ConfigurationError("CHUNK_OVERLAP must be >= 0 and smaller than CHUNK_SIZE.")
        if self.top_k < 1:
            raise ConfigurationError("TOP_K must be at least 1.")
        if self.embedding_dimension < 32:
            raise ConfigurationError("EMBEDDING_DIMENSION must be at least 32.")
        if not self.openai_model:
            raise ConfigurationError("OPENAI_MODEL must not be blank.")
        if not self.openai_embedding_model:
            raise ConfigurationError("OPENAI_EMBEDDING_MODEL must not be blank.")
        if self.mode == "openai" and not self.openai_api_key:
            raise ConfigurationError(
                "OPENAI_API_KEY is required when KNOWLEDGEBASE_MODE=openai. "
                "Copy .env.example to .env and add your key, or run in demo mode."
            )

    @classmethod
    def from_env(cls, env_file: Path | None = None) -> "Settings":
        load_dotenv(env_file or (PROJECT_ROOT / ".env"))
        return cls(
            mode=os.getenv("KNOWLEDGEBASE_MODE", "demo"),
            openai_api_key=os.getenv("OPENAI_API_KEY") or None,
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            openai_embedding_model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
            chunk_size=_int_env("CHUNK_SIZE", 400),
            chunk_overlap=_int_env("CHUNK_OVERLAP", 80),
            top_k=_int_env("TOP_K", 4),
            embedding_dimension=_int_env("EMBEDDING_DIMENSION", 256),
        )


def _int_env(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return int(raw)
    except ValueError as exc:
        raise ConfigurationError(f"{name} must be an integer.") from exc
