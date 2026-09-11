import pandas as pd

from src.core.analytics import calculate_analytics


def frame():
    return pd.DataFrame([
        {"total_amount": 1200, "quantity": 2, "status": "completed", "is_high_value": True, "category": "Software", "sales_region": "East", "product": "P", "order_date": "2026-01-01"},
        {"total_amount": 300, "quantity": 1, "status": "cancelled", "is_high_value": False, "category": "Services", "sales_region": "West", "product": "Q", "order_date": "2026-02-01"},
    ])


def test_revenue_orders_quantity_average():
    result = calculate_analytics(frame())
    assert result["total_revenue"] == 1500
    assert result["total_orders"] == 2
    assert result["total_quantity"] == 3
    assert result["average_order_value"] == 750


def test_status_and_high_value_metrics():
    result = calculate_analytics(frame())
    assert result["completed_revenue"] == 1200
    assert result["cancelled_order_count"] == 1
    assert result["high_value_order_count"] == 1


def test_grouped_metrics():
    result = calculate_analytics(frame())
    assert result["revenue_by_category"]["Software"] == 1200
    assert result["revenue_by_region"]["West"] == 300
    assert result["orders_by_status"]["completed"] == 1
    assert result["monthly_revenue"] == {"2026-01": 1200.0, "2026-02": 300.0}
