from src.data_processor import DataProcessor


def test_processor_adds_revenue_and_month(sample_frame) -> None:
    result = DataProcessor().process(sample_frame)
    assert result["revenue"].tolist() == [20, 20, 20]
    assert result["month"].tolist() == ["2025-01", "2025-01", "2025-02"]
