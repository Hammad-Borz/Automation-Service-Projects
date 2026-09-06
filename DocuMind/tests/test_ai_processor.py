import json
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from src.ai_processor import AIProcessor, AIProcessorError, MissingAPIKeyError


def client_with_content(content: str) -> MagicMock:
    client = MagicMock()
    client.chat.completions.create.return_value = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=content))]
    )
    return client


def test_requires_api_key_when_creating_client(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(MissingAPIKeyError):
        AIProcessor()


def test_processes_valid_mocked_response() -> None:
    response = json.dumps({"summary": "Summary", "key_points": ["Point"], "action_items": [], "document_category": "Memo"})
    client = client_with_content(response)
    analysis = AIProcessor(client=client).analyze("A document")
    assert analysis.document_category == "Memo"
    client.chat.completions.create.assert_called_once()


def test_wraps_provider_failure() -> None:
    client = MagicMock()
    client.chat.completions.create.side_effect = RuntimeError("provider unavailable")
    with pytest.raises(AIProcessorError, match="AI processing failed"):
        AIProcessor(client=client).analyze("A document")


def test_rejects_malformed_ai_response() -> None:
    client = client_with_content('{"summary": "Only summary"}')
    with pytest.raises(AIProcessorError, match="failed validation"):
        AIProcessor(client=client).analyze("A document")
