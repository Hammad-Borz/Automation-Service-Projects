def test_processor_calculates_revenue_and_month(processed_frame) -> None:
    assert processed_frame["revenue"].tolist() == [200.0, 250.0, 150.0]
    assert processed_frame["month"].tolist() == ["2025-01", "2025-01", "2025-02"]


def test_processor_does_not_mutate_original(raw_frame) -> None:
    original_columns = list(raw_frame.columns)
    from src.data_processor import DataProcessor
    DataProcessor().process(raw_frame)
    assert list(raw_frame.columns) == original_columns
    assert "revenue" not in raw_frame.columns
