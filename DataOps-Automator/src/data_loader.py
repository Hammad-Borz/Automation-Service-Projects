"""CSV ingestion."""

from pathlib import Path

import pandas as pd

from .exceptions import DataLoadError


class DataLoader:
    """Load supported business data files."""

    def load(self, path: Path) -> pd.DataFrame:
        path = Path(path)
        if not path.exists():
            raise DataLoadError(f"Input file does not exist: {path}")
        if path.suffix.lower() != ".csv":
            raise DataLoadError(f"Unsupported input format: {path.suffix}; expected .csv")
        try:
            frame = pd.read_csv(path)
        except (OSError, ValueError) as exc:
            raise DataLoadError(f"Could not load CSV {path}: {exc}") from exc
        if frame.empty:
            raise DataLoadError(f"Input CSV is empty: {path}")
        return frame
