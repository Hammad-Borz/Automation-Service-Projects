"""Parameterized sales database operations."""

from collections.abc import Iterable
from typing import Any

import pandas as pd

from .database_manager import DatabaseManager
from .exceptions import DatabaseError


class DataRepository:
    """Persist and retrieve normalized sales records."""

    UPSERT_SQL = """
    INSERT INTO sales (order_id, order_date, customer, region, product, category,
                       quantity, unit_price, revenue, month)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(order_id) DO UPDATE SET
        order_date = excluded.order_date, customer = excluded.customer,
        region = excluded.region, product = excluded.product,
        category = excluded.category, quantity = excluded.quantity,
        unit_price = excluded.unit_price, revenue = excluded.revenue,
        month = excluded.month
    """

    def __init__(self, database: DatabaseManager) -> None:
        self.database = database

    def insert_sales_data(self, frame: pd.DataFrame) -> int:
        records: Iterable[tuple[Any, ...]] = (
            (
                row.order_id, row.order_date.strftime("%Y-%m-%d"), row.customer,
                row.region, row.product, row.category, int(row.quantity),
                float(row.unit_price), float(row.revenue), row.month,
            )
            for row in frame.itertuples(index=False)
        )
        try:
            with self.database.connection() as connection:
                connection.executemany(self.UPSERT_SQL, records)
            return len(frame)
        except DatabaseError:
            raise

    def count_sales_records(self) -> int:
        with self.database.connection() as connection:
            row = connection.execute("SELECT COUNT(*) AS count FROM sales").fetchone()
            return int(row["count"])

    def fetch_all_sales(self) -> pd.DataFrame:
        with self.database.connection() as connection:
            return pd.read_sql_query("SELECT * FROM sales ORDER BY order_date, order_id", connection)
