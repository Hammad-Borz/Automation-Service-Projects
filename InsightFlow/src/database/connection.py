import sqlite3
from pathlib import Path


def connect(path: Path | str) -> sqlite3.Connection:
    database = Path(path)
    database.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(path: Path | str) -> None:
    with connect(path) as connection:
        connection.executescript("""
        CREATE TABLE IF NOT EXISTS sales_records (
            record_id TEXT PRIMARY KEY, order_id TEXT UNIQUE NOT NULL, customer_id TEXT NOT NULL,
            customer_name TEXT NOT NULL, customer_email TEXT, product TEXT NOT NULL, category TEXT NOT NULL,
            quantity INTEGER NOT NULL, unit_price REAL NOT NULL, total_amount REAL NOT NULL,
            calculated_total REAL NOT NULL, order_date TEXT NOT NULL, status TEXT NOT NULL,
            region TEXT NOT NULL, sales_channel TEXT NOT NULL, processed_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS analytics_runs (
            run_id TEXT PRIMARY KEY, started_at TEXT NOT NULL, completed_at TEXT,
            status TEXT NOT NULL, input_records INTEGER NOT NULL, valid_records INTEGER NOT NULL,
            invalid_records INTEGER NOT NULL, duplicate_records INTEGER NOT NULL, quality_report TEXT, reports TEXT
        );
        CREATE TABLE IF NOT EXISTS analytics_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT, run_id TEXT NOT NULL, metric_name TEXT NOT NULL,
            metric_value TEXT NOT NULL, created_at TEXT NOT NULL,
            FOREIGN KEY(run_id) REFERENCES analytics_runs(run_id)
        );
        """)
        try:
            connection.execute("ALTER TABLE analytics_runs ADD COLUMN reports TEXT")
        except sqlite3.OperationalError:
            pass
