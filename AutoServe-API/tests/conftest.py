from __future__ import annotations

import pytest

from src.database.connection import initialize_database


@pytest.fixture
def temp_db(monkeypatch, tmp_path):
    db_path = tmp_path / "autoserve_test.db"
    monkeypatch.setenv("AUTOSERVE_DB_PATH", str(db_path))
    initialize_database()
    yield db_path
    monkeypatch.delenv("AUTOSERVE_DB_PATH", raising=False)
