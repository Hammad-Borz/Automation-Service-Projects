from src.models import TaskCreate
from src.report_generator import generate_report


def test_report_includes_summary_and_grouped_titles(manager, tmp_path):
    completed = manager.create_task(TaskCreate(title="Finished work", priority="high"))
    manager.create_task(TaskCreate(title="Open work"))
    manager.complete_task(completed.id)
    report = generate_report(manager, tmp_path)
    text = report.read_text(encoding="utf-8")
    assert report.exists() and "Total tasks: 2" in text and "Finished work" in text and "Open work" in text
