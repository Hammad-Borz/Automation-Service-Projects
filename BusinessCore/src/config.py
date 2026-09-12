from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


def get_database_path() -> Path:
    configured = os.getenv("DATABASE_PATH")
    if configured:
        return Path(configured).resolve()
    return BASE_DIR / "data" / "businesscore.db"


def get_output_dir() -> Path:
    configured = os.getenv("OUTPUT_DIR")
    if configured:
        return Path(configured).resolve()
    return BASE_DIR / "data" / "output"


DATABASE_PATH = get_database_path()
OUTPUT_DIR = get_output_dir()
APP_NAME = os.getenv("APP_NAME", "BusinessCore")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
