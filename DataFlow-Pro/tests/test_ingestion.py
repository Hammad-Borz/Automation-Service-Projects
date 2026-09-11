import pandas as pd
import pytest

from src.services.ingestion_service import IngestionError, load_csv


def test_valid_csv_loading(tmp_path):
    path = tmp_path / "data.csv"
    pd.DataFrame([{"order_id": "1", "customer_name": "A", "product": "P", "category": "C", "quantity": 1, "unit_price": 2, "order_date": "2026-01-01", "status": "pending", "sales_region": "East"}]).to_csv(path, index=False)
    assert len(load_csv(path)) == 1


def test_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_csv(tmp_path / "missing.csv")


def test_missing_columns(tmp_path):
    path = tmp_path / "bad.csv"
    pd.DataFrame([{"order_id": "1"}]).to_csv(path, index=False)
    with pytest.raises(IngestionError, match="Missing required columns"):
        load_csv(path)


def test_malformed_csv(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text('order_id,customer_name\n"unterminated', encoding="utf-8")
    with pytest.raises(IngestionError):
        load_csv(path)
