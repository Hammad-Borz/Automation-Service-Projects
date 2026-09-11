import pandas as pd

from src.core.quality import build_quality_report, detect_duplicates
from src.core.validator import validate_dataframe


def test_duplicate_detection_keeps_first():
    frame = pd.DataFrame([{"order_id": "1"}, {"order_id": "1"}, {"order_id": "2"}])
    canonical, count = detect_duplicates(frame)
    assert count == 1
    assert canonical["order_id"].tolist() == ["1", "2"]


def test_quality_score_and_error_counts():
    frame = pd.DataFrame([{"order_id": "1", "customer_name": "", "product": "P", "category": "C", "quantity": 0, "unit_price": -1, "order_date": "bad", "status": "pending", "sales_region": "East"}])
    report = build_quality_report(1, validate_dataframe(frame), 0, 1)
    assert report["quality_score"] == 0.0
    assert report["invalid_records"] == 1
    assert report["invalid_quantities"] == 1
    assert report["invalid_prices"] == 1
