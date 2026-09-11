from pathlib import Path

import pandas as pd

from src.core.validator import validate_columns


class IngestionError(ValueError):
    pass


def load_csv(path: Path, required_columns: set[str] | None = None) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    try:
        frame = pd.read_csv(path)
    except (OSError, pd.errors.ParserError) as exc:
        raise IngestionError(f"Unable to read CSV: {exc}") from exc
    missing = validate_columns([str(column).strip().lower() for column in frame.columns]) if required_columns is None else sorted(required_columns - set(frame.columns))
    if missing:
        raise IngestionError(f"Missing required columns: {', '.join(missing)}")
    return frame
