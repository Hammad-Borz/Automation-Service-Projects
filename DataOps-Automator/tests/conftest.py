from pathlib import Path

import pandas as pd
import pytest

from src.config import Settings
from src.data_processor import DataProcessor
from src.database_manager import DatabaseManager
from src.data_repository import DataRepository


@pytest.fixture
def raw_frame() -> pd.DataFrame:
    return pd.DataFrame({
        "order_id": ["A-1", "A-2", "A-3"],
        "order_date": ["2025-01-02", "2025-01-15", "2025-02-03"],
        "customer": ["Acme North", "Acme South", "Acme North"],
        "region": ["North", "South", "North"],
        "product": ["Suite", "Suite", "Consulting"],
        "category": ["Software", "Software", "Services"],
        "quantity": [2, 1, 3],
        "unit_price": [100, 250, 50],
    })


@pytest.fixture
def processed_frame(raw_frame: pd.DataFrame) -> pd.DataFrame:
    return DataProcessor().process(raw_frame)


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    return Settings.from_project_root(tmp_path)


@pytest.fixture
def repository(settings: Settings) -> DataRepository:
    database = DatabaseManager(settings.database_path)
    database.initialize_schema()
    return DataRepository(database)
