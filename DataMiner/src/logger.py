"""Logging setup for DataMiner."""

from __future__ import annotations

import logging
from pathlib import Path


def get_logger(name: str = "dataminer", log_file: str | Path = "logs/dataminer.log") -> logging.Logger:
    """Return a file logger while avoiding duplicate handlers."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    target = Path(log_file).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    if not any(isinstance(item, logging.FileHandler) and Path(item.baseFilename).resolve() == target for item in logger.handlers):
        handler = logging.FileHandler(target, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
        logger.addHandler(handler)
    return logger
