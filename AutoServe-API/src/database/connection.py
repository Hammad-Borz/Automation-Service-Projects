from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterator

from src.config import get_database_path


def get_connection() -> sqlite3.Connection:
    """Create a SQLite connection with row factory and safe defaults."""
    db_path = get_database_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(db_path))
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA journal_mode = WAL")
    return connection


def initialize_database() -> None:
    """Create the required schema for the application if missing."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS automation_jobs (
                id TEXT PRIMARY KEY,
                request_id TEXT NOT NULL UNIQUE,
                automation_type TEXT NOT NULL,
                payload TEXT NOT NULL,
                status TEXT NOT NULL,
                retry_count INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS automation_runs (
                id TEXT PRIMARY KEY,
                job_id TEXT NOT NULL,
                status TEXT NOT NULL,
                attempt_number INTEGER NOT NULL,
                started_at TEXT NOT NULL,
                completed_at TEXT,
                error_message TEXT,
                FOREIGN KEY (job_id) REFERENCES automation_jobs(id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS action_results (
                id TEXT PRIMARY KEY,
                run_id TEXT NOT NULL,
                action_type TEXT NOT NULL,
                success BOOLEAN NOT NULL,
                result TEXT NOT NULL,
                error_message TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_logs (
                id TEXT PRIMARY KEY,
                job_id TEXT,
                run_id TEXT,
                event_type TEXT NOT NULL,
                message TEXT NOT NULL,
                metadata TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()
