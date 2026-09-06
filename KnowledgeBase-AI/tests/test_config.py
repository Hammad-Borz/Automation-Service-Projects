from src.config import Settings
from src.exceptions import ConfigurationError
import pytest


def test_rejects_invalid_mode() -> None:
    with pytest.raises(ConfigurationError, match="KNOWLEDGEBASE_MODE"):
        Settings(mode="prod")


def test_rejects_openai_mode_without_key() -> None:
    with pytest.raises(ConfigurationError, match="OPENAI_API_KEY"):
        Settings(mode="openai", openai_api_key=None)


def test_rejects_bad_chunk_overlap() -> None:
    with pytest.raises(ConfigurationError, match="CHUNK_OVERLAP"):
        Settings(chunk_size=100, chunk_overlap=100)
