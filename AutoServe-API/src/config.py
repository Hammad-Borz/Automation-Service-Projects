from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = PROJECT_ROOT / "data" / "autoserve.db"

APP_NAME = "AutoServe API"
APP_VERSION = "0.1.0"
MAX_RETRY_COUNT = 3
ENVIRONMENT = os.getenv("AUTOSERVE_ENVIRONMENT", "local")


def get_database_path() -> Path:
    """Return the configured SQLite path, allowing tests and local overrides."""
    configured = os.getenv("AUTOSERVE_DB_PATH")
    if configured:
        return Path(configured)
    return DEFAULT_DB_PATH


def get_database_path_str() -> str:
    return str(get_database_path())
