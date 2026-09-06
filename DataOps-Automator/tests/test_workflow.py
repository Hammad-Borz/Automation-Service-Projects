from pathlib import Path

from src.workflow import DataOpsWorkflow


def test_complete_workflow_is_repeatable(settings) -> None:
    source = Path(__file__).parents[1] / "data" / "input" / "sales_data.csv"
    workflow = DataOpsWorkflow(settings)
    first = workflow.run(source)
    second = workflow.run(source)
    assert first.records_processed == 16
    assert first.database_records == 16
    assert second.database_records == 16
    assert settings.database_path.exists()
    assert all(path.exists() for path in second.report_paths)
