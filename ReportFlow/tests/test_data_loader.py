from pathlib import Path

import pandas as pd
import pytest

from src.data_loader import DataLoader
from src.exceptions import DataLoadError


def test_load_csv(tmp_path: Path) -> None:
    path = tmp_path / "orders.csv"
    pd.DataFrame({"order_id": ["1"]}).to_csv(path, index=False)
    assert DataLoader().load(path).shape == (1, 1)


def test_reject_missing_file(tmp_path: Path) -> None:
    with pytest.raises(DataLoadError, match="does not exist"):
        DataLoader().load(tmp_path / "missing.csv")


def test_reject_unsupported_format(tmp_path: Path) -> None:
    path = tmp_path / "orders.json"
    path.write_text("{}")
    with pytest.raises(DataLoadError, match="Unsupported"):
        DataLoader().load(path)
