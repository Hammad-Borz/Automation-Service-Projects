"""Human-readable processing report generation."""

from __future__ import annotations

from pathlib import Path


class ReportGenerator:
    """Persist a summary for each completed processing run."""

    def __init__(self, reports_dir: str | Path = "reports") -> None:
        self.reports_dir = Path(reports_dir)

    def generate(self, source_url: str, summary: dict[str, int], csv_path: Path, json_path: Path) -> Path:
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        report_path = self.reports_dir / "processing_report.txt"
        lines = [
            "DataMiner Processing Report",
            "=" * 27,
            f"Source URL: {source_url}",
            f"Total extracted: {summary['total_extracted']}",
            f"Valid records: {summary['valid_records']}",
            f"Invalid records: {summary['invalid_records']}",
            f"Successfully cleaned records: {summary['successfully_cleaned_records']}",
            f"Failed cleaning records: {summary['failed_cleaning_records']}",
            f"CSV export location: {csv_path}",
            f"JSON export location: {json_path}",
        ]
        report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return report_path
