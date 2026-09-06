from pathlib import Path

import pandas as pd
import pytest

from src.data_loader import DataLoader
from src.exceptions import DataLoadError


def test_load_csv(tmp_path: Path, raw_frame: pd.DataFrame) -> None:
    path = tmp_path / "sales.csv"
    raw_frame.to_csv(path, index=False)
    loaded = DataLoader().load(path)
    assert loaded.equals(raw_frame)


def test_missing_file_rejected(tmp_path: Path) -> None:
    with pytest.raises(DataLoadError, match="does not exist"):
        DataLoader().load(tmp_path / "missing.csv")


def test_unsupported_file_rejected(tmp_path: Path) -> None:
    path = tmp_path / "sales.json"
    path.write_text("{}", encoding="utf-8")
    with pytest.raises(DataLoadError, match="Unsupported"):
        DataLoader().load(path)
