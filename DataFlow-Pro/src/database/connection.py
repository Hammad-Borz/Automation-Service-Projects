import sqlite3
from pathlib import Path


def connect(database_path: Path | str) -> sqlite3.Connection:
    path = Path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(database_path: Path | str) -> None:
    with connect(database_path) as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS business_records (
                record_id TEXT PRIMARY KEY,
                order_id TEXT NOT NULL UNIQUE,
                customer_name TEXT NOT NULL,
                customer_email TEXT,
                company TEXT,
                product TEXT NOT NULL,
                category TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                total_amount REAL NOT NULL,
                currency TEXT NOT NULL,
                order_date TEXT NOT NULL,
                status TEXT NOT NULL,
                sales_region TEXT NOT NULL,
                source TEXT NOT NULL,
                is_high_value INTEGER NOT NULL,
                processed_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS processing_runs (
                run_id TEXT PRIMARY KEY,
                started_at TEXT NOT NULL,
                completed_at TEXT,
                input_records INTEGER NOT NULL,
                valid_records INTEGER NOT NULL,
                invalid_records INTEGER NOT NULL,
                duplicate_records INTEGER NOT NULL,
                status TEXT NOT NULL,
                quality_report TEXT
            );
            """
        )
        try:
            connection.execute("ALTER TABLE processing_runs ADD COLUMN quality_report TEXT")
        except sqlite3.OperationalError:
            pass
