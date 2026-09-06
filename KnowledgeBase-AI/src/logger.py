"""Application logging configured for local, non-sensitive diagnostics."""

from __future__ import annotations

import logging
from pathlib import Path


def get_logger(log_dir: str | Path | None = None) -> logging.Logger:
    """Return the KnowledgeBase AI file logger without stacking duplicate handlers."""
    logger = logging.getLogger("knowledgebase_ai")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    logger.propagate = False
    directory = Path(log_dir) if log_dir else Path(__file__).resolve().parents[1] / "logs"
    directory.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(directory / "knowledgebase_ai.log", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    logger.addHandler(handler)
    return logger
