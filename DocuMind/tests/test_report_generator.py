from pathlib import Path

from src.models import DocumentAnalysis
from src.report_generator import ReportGenerator


def test_generates_human_readable_report(tmp_path: Path) -> None:
    analysis = DocumentAnalysis(summary="Reviewed contract.", key_points=["Renewal", "Price"], action_items=["Respond"], document_category="Contract")
    target = ReportGenerator(tmp_path).generate(analysis, "contract.docx")
    report = target.read_text(encoding="utf-8")
    assert target.name == "contract_report.txt"
    assert "Source document: contract.docx" in report
    assert "Number of key points: 2" in report
    assert "Number of action items: 1" in report
