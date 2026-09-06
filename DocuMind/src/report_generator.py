"""Human-readable processing reports."""

from pathlib import Path

from .models import DocumentAnalysis
from .result_exporter import ResultExporter


class ReportGenerator:
    """Generate concise plain-text reports for completed processing runs."""

    def __init__(self, output_dir: str | Path) -> None:
        self.output_dir = Path(output_dir)

    def generate(self, analysis: DocumentAnalysis, source_name: str, status: str = "Success") -> Path:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        report = "\n".join(
            [
                "DocuMind Processing Report",
                "=" * 28,
                f"Source document: {source_name}",
                f"Processing status: {status}",
                f"Document category: {analysis.document_category}",
                f"Summary: {analysis.summary}",
                f"Number of key points: {len(analysis.key_points)}",
                f"Number of action items: {len(analysis.action_items)}",
                "",
            ]
        )
        target = self.output_dir / f"{ResultExporter.safe_stem(source_name)}_report.txt"
        target.write_text(report, encoding="utf-8")
        return target
