from __future__ import annotations

import os
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def isolated_database(monkeypatch, tmp_path):
    db_path = tmp_path / "businesscore_test.db"
    monkeypatch.setenv("DATABASE_PATH", str(db_path))
    yield
    try:
        if db_path.exists():
            db_path.unlink()
    except PermissionError:
        pass
