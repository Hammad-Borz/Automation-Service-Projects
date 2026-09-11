import pandas as pd

from src.core.cleaner import clean_dataframe


def test_cleaning_normalizes_text():
    frame = pd.DataFrame([{"order_id": " 1 ", "customer_name": " jane doe ", "product": " data suite ", "category": " SOFTWARE ", "quantity": 1, "unit_price": 2, "order_date": "2026-01-01", "status": " COMPLETED ", "sales_region": " north america ", "customer_email": " JANE@EXAMPLE.COM ", "currency": "usd"}])
    result = clean_dataframe(frame, "source.csv").iloc[0]
    assert result["customer_name"] == "Jane Doe"
    assert result["product"] == "Data Suite"
    assert result["status"] == "completed"
    assert result["currency"] == "USD"
    assert result["customer_email"] == "jane@example.com"
    assert result["sales_region"] == "North America"


def test_missing_currency_defaults_to_usd():
    frame = pd.DataFrame([{"order_id": "1", "customer_name": "A", "product": "P", "category": "C", "quantity": 1, "unit_price": 2, "order_date": "2026-01-01", "status": "pending", "sales_region": "East"}])
    assert clean_dataframe(frame, "x").iloc[0]["currency"] == "USD"


def test_empty_strings_become_none():
    frame = pd.DataFrame([{"order_id": "1", "customer_name": "", "product": "P", "category": "C", "quantity": 1, "unit_price": 2, "order_date": "2026-01-01", "status": "pending", "sales_region": "East"}])
    assert clean_dataframe(frame, "x").iloc[0]["customer_name"] is None
