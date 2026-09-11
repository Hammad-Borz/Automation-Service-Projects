from pathlib import Path
from src.core.data_loader import load_csv


def ingest(path: Path):
    return load_csv(path)
