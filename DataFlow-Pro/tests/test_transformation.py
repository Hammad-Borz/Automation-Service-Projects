import pandas as pd

from src.core.transformer import transform_dataframe


def test_total_and_high_value_calculation():
    frame = pd.DataFrame([{"order_date": "2026-01-02", "quantity": 2, "unit_price": 600, "status": "completed"}])
    result = transform_dataframe(frame, 1000).iloc[0]
    assert result["total_amount"] == 1200
    assert result["calculated_total"] == 1200
    assert bool(result["is_high_value"])


def test_derived_month_and_year():
    frame = pd.DataFrame([{"order_date": "2026-03-02", "quantity": 1, "unit_price": 1}])
    result = transform_dataframe(frame, 1000).iloc[0]
    assert result["order_month"] == "2026-03"
    assert result["order_year"] == 2026


def test_low_value_is_not_high_value():
    frame = pd.DataFrame([{"order_date": "2026-01-02", "quantity": 1, "unit_price": 10}])
    assert not bool(transform_dataframe(frame, 1000).iloc[0]["is_high_value"])
