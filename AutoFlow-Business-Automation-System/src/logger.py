"""Configure persistent logging for AutoFlow."""

import logging
from pathlib import Path


def setup_logger() -> logging.Logger:
    """Return the application logger with a file handler attached once."""
    project_folder = Path(__file__).resolve().parent.parent
    logs_folder = project_folder / "logs"
    logs_folder.mkdir(parents=True, exist_ok=True)

    log_file = logs_folder / "autoflow.log"

    logger = logging.getLogger("autoflow")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
