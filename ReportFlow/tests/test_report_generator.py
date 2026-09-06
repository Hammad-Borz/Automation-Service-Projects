from src.analytics import Analytics
from src.data_processor import DataProcessor
from src.report_generator import ReportGenerator


def test_text_report_contains_executive_summary(sample_frame, tmp_path) -> None:
    analytics = Analytics().calculate(DataProcessor().process(sample_frame))
    path = ReportGenerator().generate(analytics, tmp_path / "report.txt")
    content = path.read_text(encoding="utf-8")
    assert "EXECUTIVE SUMMARY" in content
    assert "$60.00" in content
    assert "MONTHLY PERFORMANCE" in content
