"""Central logging configuration."""

import logging
from pathlib import Path


def get_logger(log_dir: str | Path) -> logging.Logger:
    """Return DocuMind's file logger without stacking duplicate handlers."""
    logger = logging.getLogger("documind")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    log_path = Path(log_dir) / "documind.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if not any(isinstance(h, logging.FileHandler) and Path(h.baseFilename) == log_path.resolve() for h in logger.handlers):
        handler = logging.FileHandler(log_path, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
        logger.addHandler(handler)
    return logger
