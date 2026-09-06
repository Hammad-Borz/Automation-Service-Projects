"""Shared fixtures for DataMiner tests."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest


@pytest.fixture
def tmp_path() -> Iterator[Path]:
    """Provide an isolated directory without pytest's shared base-temp cleanup.

    ``TemporaryDirectory`` creates and removes one directory per test. This
    avoids Windows permission errors caused by pytest retaining and deleting a
    project-wide base directory between test sessions.
    """
    with TemporaryDirectory(prefix="dataminer-test-", dir=Path(__file__).parent) as directory:
        yield Path(directory)
