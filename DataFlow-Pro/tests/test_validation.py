import pandas as pd

from src.core.validator import validate_dataframe, validate_columns


def base(**overrides):
    row = {"order_id": "1", "customer_name": "A", "product": "P", "category": "C", "quantity": 1, "unit_price": 2, "order_date": "2026-01-01", "status": "pending", "sales_region": "East", "customer_email": "a@example.com"}
    row.update(overrides)
    return pd.DataFrame([row])


def test_valid_record():
    assert validate_dataframe(base())[0].valid


def test_missing_required_value():
    result = validate_dataframe(base(customer_name=""))[0]
    assert "customer_name is required" in result.errors


def test_invalid_quantity():
    assert not validate_dataframe(base(quantity=0))[0].valid


def test_invalid_price():
    assert not validate_dataframe(base(unit_price=-1))[0].valid


def test_invalid_email():
    assert "customer_email is invalid" in validate_dataframe(base(customer_email="bad"))[0].errors


def test_invalid_status_and_date():
    result = validate_dataframe(base(status="shipped", order_date="bad"))[0]
    assert "status is unsupported" in result.errors
    assert "order_date is invalid" in result.errors


def test_missing_columns_reports_names():
    assert "product" in validate_columns(["order_id"])
