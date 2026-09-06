import sqlite3

from src.database_manager import DatabaseManager


def test_database_and_schema_are_created(settings) -> None:
    manager = DatabaseManager(settings.database_path)
    manager.initialize_schema()
    assert settings.database_path.exists()
    with manager.connection() as connection:
        table = connection.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sales'").fetchone()
    assert table[0] == "sales"


def test_connection_rolls_back_on_sql_error(settings) -> None:
    manager = DatabaseManager(settings.database_path)
    manager.initialize_schema()
    try:
        with manager.connection() as connection:
            connection.execute("INSERT INTO missing_table VALUES (1)")
    except Exception as exc:
        assert "Database operation failed" in str(exc)
    with manager.connection() as connection:
        assert connection.execute("SELECT COUNT(*) FROM sales").fetchone()[0] == 0
