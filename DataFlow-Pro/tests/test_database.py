import pandas as pd

from src.database.connection import initialize_database
from src.database.repository import DataRepository


def record(order_id="1", price=10):
    return pd.DataFrame([{"record_id": order_id, "order_id": order_id, "customer_name": "A", "customer_email": None, "company": "C", "product": "P", "category": "Cat", "quantity": 1, "unit_price": price, "total_amount": price, "currency": "USD", "order_date": "2026-01-01", "status": "completed", "sales_region": "East", "source": "x", "is_high_value": False}])


def test_database_initialization(tmp_path):
    path = tmp_path / "db.sqlite3"
    initialize_database(path)
    assert path.exists()


def test_insert_and_retrieve(tmp_path):
    repository = DataRepository(tmp_path / "db.sqlite3")
    repository.upsert_records(record())
    assert repository.get_record("1")["total_amount"] == 10


def test_upsert_updates_by_order_id(tmp_path):
    repository = DataRepository(tmp_path / "db.sqlite3")
    repository.upsert_records(record(price=10))
    repository.upsert_records(record(price=25))
    assert repository.get_record("1")["total_amount"] == 25
    assert len(repository.list_records()) == 1


def test_processing_run_persistence(tmp_path):
    repository = DataRepository(tmp_path / "db.sqlite3")
    run = {"run_id": "run-1", "started_at": "now", "completed_at": "later", "input_records": 1, "valid_records": 1, "invalid_records": 0, "duplicate_records": 0, "status": "completed"}
    repository.save_run(run)
    assert repository.get_run("run-1")["status"] == "completed"
    assert len(repository.list_runs()) == 1
