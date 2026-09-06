from src.analytics import Analytics
from src.data_processor import DataProcessor


def test_calculate_kpis_and_rankings(sample_frame) -> None:
    result = Analytics().calculate(DataProcessor().process(sample_frame))
    assert result.kpis == {"total_revenue": 60.0, "total_orders": 3, "total_units": 7, "average_order_value": 20.0}
    assert result.by_product.iloc[0]["product"] == "A"
    assert result.monthly.iloc[0]["month"] == "2025-01"
