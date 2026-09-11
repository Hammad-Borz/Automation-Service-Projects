from pathlib import Path
import pandas as pd
import pytest
from fastapi.testclient import TestClient
from src.config import Settings
from src.main import create_app

@pytest.fixture
def settings(tmp_path: Path):
    root = tmp_path / "project"; (root / "data" / "input").mkdir(parents=True); (root / "data" / "output").mkdir(parents=True)
    return Settings(root, root / "data", root / "data/input", root / "data/output", root / "data/test.sqlite3", root / "data/input/sales.csv")

@pytest.fixture
def frame():
    return pd.DataFrame([
        {"order_id":"1","customer_id":"c1","customer_name":" Alice ","customer_email":"ALICE@EXAMPLE.COM","product":"Suite","category":"software","quantity":2,"unit_price":600,"total_amount":1,"order_date":"2026-01-02","status":" COMPLETED ","region":" north america ","sales_channel":"ONLINE"},
        {"order_id":"2","customer_id":"c2","customer_name":"Bob","customer_email":"bob@example.com","product":"Connector","category":"services","quantity":1,"unit_price":200,"total_amount":200,"order_date":"2026-02-02","status":"completed","region":"Europe","sales_channel":"retail"},
    ])

@pytest.fixture
def client(settings, frame):
    frame.to_csv(settings.default_input_path, index=False)
    return TestClient(create_app(settings), raise_server_exceptions=False)
