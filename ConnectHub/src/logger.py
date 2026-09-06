"""Logging configuration for ConnectHub."""

from __future__ import annotations

import logging
from pathlib import Path


def get_logger(name: str = "connecthub", log_file: str | Path = "logs/connecthub.log") -> logging.Logger:
    """Return a configured logger without adding duplicate handlers."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    path = Path(log_file).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    if not any(isinstance(handler, logging.FileHandler) and Path(handler.baseFilename).resolve() == path for handler in logger.handlers):
        handler = logging.FileHandler(path, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
        logger.addHandler(handler)
    return logger
