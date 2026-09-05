"""Generate a human-readable automation report."""

from pathlib import Path


def generate_report(processed_files: list[dict]) -> Path:
    """Write processed file metrics to the reports directory."""
    project_folder = Path(__file__).resolve().parent.parent
    reports_folder = project_folder / "reports"
    reports_folder.mkdir(parents=True, exist_ok=True)

    report_path = reports_folder / "automation_report.txt"

    with report_path.open("w", encoding="utf-8") as report:
        report.write("AUTO FLOW BUSINESS AUTOMATION REPORT\n")
        report.write("=" * 40 + "\n\n")
        report.write(f"Total files processed: {len(processed_files)}\n\n")

        for file_data in processed_files:
            report.write(f"File: {file_data['file_name']}\n")
            report.write(f"Type: {file_data['file_type']}\n")

            if file_data["file_type"] == "Text":
                report.write(f"Lines: {file_data['line_count']}\n")
                report.write(f"Words: {file_data['word_count']}\n")
            elif file_data["file_type"] == "CSV":
                report.write(f"Columns: {', '.join(file_data['columns'])}\n")
                report.write(f"Rows: {file_data['row_count']}\n")

            report.write("-" * 40 + "\n")

    return report_path
