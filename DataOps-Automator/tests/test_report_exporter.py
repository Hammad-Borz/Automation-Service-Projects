from src.analytics import Analytics
from src.report_exporter import ReportExporter


def test_required_csv_reports_and_text_report_are_created(repository, processed_frame, tmp_path) -> None:
    repository.insert_sales_data(processed_frame)
    analytics = Analytics(repository.database).calculate()
    paths = ReportExporter().export(analytics, tmp_path)
    expected = {
        "kpi_summary.csv", "revenue_by_region.csv", "revenue_by_product.csv",
        "revenue_by_category.csv", "monthly_revenue.csv", "top_products.csv",
        "business_report.txt",
    }
    assert {path.name for path in paths} == expected
    report = (tmp_path / "business_report.txt").read_text(encoding="utf-8")
    assert "EXECUTIVE SUMMARY" in report
    assert "Total revenue: $600.00" in report
    assert "Top region: North" in report
