"""JSON persistence for successful analysis results."""

import json
import re
from pathlib import Path

from .models import DocumentAnalysis


class ResultExporter:
    """Save validated analyses under deterministic, filesystem-safe names."""

    def __init__(self, output_dir: str | Path) -> None:
        self.output_dir = Path(output_dir)

    @staticmethod
    def safe_stem(source_name: str) -> str:
        stem = Path(source_name).stem
        safe = re.sub(r"[^A-Za-z0-9_-]+", "_", stem).strip("._-")
        return safe or "document"

    def export(self, analysis: DocumentAnalysis, source_name: str) -> Path:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        target = self.output_dir / f"{self.safe_stem(source_name)}_analysis.json"
        target.write_text(json.dumps(analysis.model_dump(), indent=2, ensure_ascii=False), encoding="utf-8")
        return target
