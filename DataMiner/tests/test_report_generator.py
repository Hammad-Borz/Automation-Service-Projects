from report_generator import ReportGenerator


def test_generates_human_readable_report(tmp_path):
    summary = {"total_extracted": 3, "valid_records": 2, "invalid_records": 1, "successfully_cleaned_records": 1, "failed_cleaning_records": 1}
    path = ReportGenerator(tmp_path / "reports").generate("https://example.test/catalog", summary, tmp_path / "products.csv", tmp_path / "products.json")
    content = path.read_text(encoding="utf-8")
    assert path.exists()
    assert "Source URL: https://example.test/catalog" in content
    assert "Successfully cleaned records: 1" in content
