from pathlib import Path

import pandas as pd
import pytest
from fastapi.testclient import TestClient

from src.config import Settings
from src.main import create_app


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    root = tmp_path / "project"
    (root / "data" / "input").mkdir(parents=True)
    (root / "data" / "output").mkdir(parents=True)
    return Settings(root, root / "data" / "test.sqlite3", root / "data" / "input" / "input.csv", root / "data" / "output")


@pytest.fixture
def valid_frame() -> pd.DataFrame:
    return pd.DataFrame([{
        "order_id": "ORD-1", "customer_name": " Alice ", "customer_email": "ALICE@EXAMPLE.COM",
        "company": "Acme", "product": "Analytics Suite", "category": "software", "quantity": 2,
        "unit_price": 750, "total_amount": 1, "currency": "usd", "order_date": "2026-01-15",
        "status": " COMPLETED ", "sales_region": " north america ",
    }])


@pytest.fixture
def client(settings, valid_frame):
    settings.default_input_path.parent.mkdir(parents=True, exist_ok=True)
    valid_frame.to_csv(settings.default_input_path, index=False)
    return TestClient(create_app(settings), raise_server_exceptions=False)
