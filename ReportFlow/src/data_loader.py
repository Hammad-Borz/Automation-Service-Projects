"""CSV and Excel ingestion."""

from pathlib import Path

import pandas as pd

from .exceptions import DataLoadError


class DataLoader:
    """Load supported tabular files into a DataFrame."""

    SUPPORTED_SUFFIXES = {".csv", ".xlsx"}

    def load(self, path: Path) -> pd.DataFrame:
        path = Path(path)
        if not path.exists():
            raise DataLoadError(f"Input file does not exist: {path}")
        if path.suffix.lower() not in self.SUPPORTED_SUFFIXES:
            raise DataLoadError(f"Unsupported input format: {path.suffix}")
        try:
            frame = pd.read_csv(path) if path.suffix.lower() == ".csv" else pd.read_excel(path)
        except (OSError, ValueError, ImportError) as exc:
            raise DataLoadError(f"Could not load {path}: {exc}") from exc
        if frame.empty:
            raise DataLoadError(f"Input file is empty: {path}")
        return frame
