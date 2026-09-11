import pytest
from fastapi.testclient import TestClient

from src.config import Settings
from src.main import create_app


@pytest.fixture
def client(tmp_path):
    return TestClient(
        create_app(Settings(database_path=str(tmp_path / "test.sqlite3"))),
        raise_server_exceptions=False,
    )


@pytest.fixture
def payload():
    return {
        "event_id": "evt-1001",
        "event_type": "lead.created",
        "timestamp": "2026-09-11T10:30:00Z",
        "source": "website",
        "data": {"name": "John Doe", "email": "john@example.com", "message": "Interested in a demo"},
    }
