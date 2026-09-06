from pathlib import Path

from src.workflow import ReportingWorkflow


def test_end_to_end_workflow(settings) -> None:
    source = Path(__file__).parents[1] / "data" / "input" / "sales_data.csv"
    result = ReportingWorkflow(settings).run(source)
    assert result.analytics.kpis["total_orders"] == 15
    assert result.excel_report.exists()
    assert result.text_report.exists()
    assert len(result.csv_exports) == 4
    assert all(path.exists() for path in result.csv_exports)
