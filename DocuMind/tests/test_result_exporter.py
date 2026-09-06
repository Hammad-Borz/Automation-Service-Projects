import json
from pathlib import Path

from src.models import DocumentAnalysis
from src.result_exporter import ResultExporter


def test_exports_valid_json_with_safe_name(tmp_path: Path) -> None:
    analysis = DocumentAnalysis(summary="Done", key_points=["P"], action_items=[], document_category="Memo")
    target = ResultExporter(tmp_path).export(analysis, "Quarterly report (final).pdf")
    assert target.name == "Quarterly_report_final_analysis.json"
    assert json.loads(target.read_text(encoding="utf-8"))["summary"] == "Done"
