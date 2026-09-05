"""Process supported business files into structured metrics."""

import csv
from pathlib import Path


def process_text_file(file_path: Path) -> dict:
    """Return basic text-file metrics."""
    content = file_path.read_text(encoding="utf-8")

    return {
        "file_name": file_path.name,
        "file_type": "Text",
        "line_count": len(content.splitlines()),
        "word_count": len(content.split()),
    }


def process_csv_file(file_path: Path) -> dict:
    """Return CSV headers and data-row count."""
    with file_path.open(encoding="utf-8", newline="") as file:
        rows = list(csv.reader(file))

    headers = rows[0] if rows else []
    data_rows = rows[1:] if len(rows) > 1 else []

    return {
        "file_name": file_path.name,
        "file_type": "CSV",
        "columns": headers,
        "row_count": len(data_rows),
    }
