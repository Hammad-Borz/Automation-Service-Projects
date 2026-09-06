"""SQLite connection and schema lifecycle management."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from .exceptions import DatabaseError
from .schema import CREATE_SALES_TABLE


class DatabaseManager:
    """Manage SQLite connections, transactions, and schema setup."""

    def __init__(self, database_path: Path) -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def connection(self) -> Iterator[sqlite3.Connection]:
        connection: sqlite3.Connection | None = None
        try:
            connection = sqlite3.connect(self.database_path)
            connection.row_factory = sqlite3.Row
            connection.execute("PRAGMA foreign_keys = ON")
            yield connection
            connection.commit()
        except sqlite3.Error as exc:
            if connection is not None:
                connection.rollback()
            raise DatabaseError(f"Database operation failed: {exc}") from exc
        finally:
            if connection is not None:
                connection.close()

    def initialize_schema(self) -> None:
        try:
            with self.connection() as connection:
                connection.execute(CREATE_SALES_TABLE)
        except DatabaseError:
            raise
