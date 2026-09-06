from pathlib import Path

import pandas as pd
import pytest

from src.config import Settings


@pytest.fixture
def sample_frame() -> pd.DataFrame:
    return pd.DataFrame({
        "order_id": ["1", "2", "3"],
        "order_date": ["2025-01-01", "2025-01-15", "2025-02-01"],
        "product": ["A", "A", "B"],
        "category": ["Software", "Software", "Services"],
        "region": ["North", "South", "North"],
        "quantity": [2, 1, 4],
        "unit_price": [10, 20, 5],
    })


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    return Settings.from_project_root(tmp_path)
