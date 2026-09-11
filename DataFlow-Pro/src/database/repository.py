import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from src.database.connection import connect, initialize_database


class DataRepository:
    def __init__(self, database_path: Path | str) -> None:
        self.database_path = Path(database_path)
        initialize_database(self.database_path)

    def upsert_records(self, records: pd.DataFrame) -> int:
        if records.empty:
            return 0
        columns = ["record_id", "order_id", "customer_name", "customer_email", "company", "product", "category", "quantity", "unit_price", "total_amount", "currency", "order_date", "status", "sales_region", "source", "is_high_value"]
        sql = f"""INSERT INTO business_records ({', '.join(columns)}, processed_at)
            VALUES ({', '.join('?' for _ in columns)}, ?)
            ON CONFLICT(order_id) DO UPDATE SET
            {', '.join(f'{column}=excluded.{column}' for column in columns if column != 'order_id')}, processed_at=excluded.processed_at"""
        now = datetime.now(timezone.utc).isoformat()
        with connect(self.database_path) as connection:
            for row in records[columns].itertuples(index=False, name=None):
                values = tuple(value.item() if hasattr(value, "item") else value for value in row)
                connection.execute(sql, values + (now,))
        return len(records)

    def save_run(self, run: dict[str, Any]) -> None:
        with connect(self.database_path) as connection:
            connection.execute(
                """INSERT OR REPLACE INTO processing_runs
                (run_id, started_at, completed_at, input_records, valid_records, invalid_records, duplicate_records, status, quality_report)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (run["run_id"], run["started_at"], run.get("completed_at"), run["input_records"], run["valid_records"], run["invalid_records"], run["duplicate_records"], run["status"], json.dumps(run.get("quality", {}))),
            )

    def get_run(self, run_id: str) -> dict[str, Any] | None:
        with connect(self.database_path) as connection:
            row = connection.execute("SELECT * FROM processing_runs WHERE run_id = ?", (run_id,)).fetchone()
        return self._deserialize_run(row) if row else None

    def list_runs(self) -> list[dict[str, Any]]:
        with connect(self.database_path) as connection:
            rows = connection.execute("SELECT * FROM processing_runs ORDER BY started_at DESC").fetchall()
        return [self._deserialize_run(row) for row in rows]

    def list_records(self, limit: int = 100, offset: int = 0) -> list[dict[str, Any]]:
        with connect(self.database_path) as connection:
            rows = connection.execute("SELECT * FROM business_records ORDER BY order_date DESC LIMIT ? OFFSET ?", (limit, offset)).fetchall()
        return [dict(row) for row in rows]

    def get_record(self, order_id: str) -> dict[str, Any] | None:
        with connect(self.database_path) as connection:
            row = connection.execute("SELECT * FROM business_records WHERE order_id = ?", (order_id,)).fetchone()
        return dict(row) if row else None

    @staticmethod
    def _deserialize_run(row: Any) -> dict[str, Any]:
        result = dict(row)
        result["quality"] = json.loads(result.pop("quality_report") or "{}")
        return result

    def latest_quality(self) -> dict[str, Any] | None:
        with connect(self.database_path) as connection:
            row = connection.execute("SELECT * FROM processing_runs ORDER BY started_at DESC LIMIT 1").fetchone()
        return self._deserialize_run(row) if row else None
