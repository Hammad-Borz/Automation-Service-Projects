"""CSV and JSON exports for cleaned records."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ExportPaths:
    csv_path: Path
    json_path: Path


class DataExporter:
    """Write records to portable CSV and JSON files."""

    FIELDNAMES = ("name", "price", "category", "availability")

    def __init__(self, output_dir: str | Path = "output") -> None:
        self.output_dir = Path(output_dir)

    def export(self, records: list[dict[str, Any]]) -> ExportPaths:
        csv_dir = self.output_dir / "csv"
        json_dir = self.output_dir / "json"
        csv_dir.mkdir(parents=True, exist_ok=True)
        json_dir.mkdir(parents=True, exist_ok=True)
        csv_path = csv_dir / "products.csv"
        json_path = json_dir / "products.json"
        with csv_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.FIELDNAMES)
            writer.writeheader()
            writer.writerows(records)
        with json_path.open("w", encoding="utf-8") as file:
            json.dump(records, file, ensure_ascii=False, indent=2)
        return ExportPaths(csv_path, json_path)
