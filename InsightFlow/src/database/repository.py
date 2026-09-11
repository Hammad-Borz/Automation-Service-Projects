import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import pandas as pd
from src.database.connection import connect, initialize_database


class AnalyticsRepository:
    def __init__(self, path: Path | str):
        self.path = Path(path); initialize_database(self.path)

    def upsert_records(self, frame: pd.DataFrame) -> int:
        columns = ["record_id", "order_id", "customer_id", "customer_name", "customer_email", "product", "category", "quantity", "unit_price", "total_amount", "calculated_total", "order_date", "status", "region", "sales_channel"]
        if frame.empty: return 0
        sql = f"INSERT INTO sales_records ({', '.join(columns)}, processed_at) VALUES ({', '.join('?' for _ in columns)}, ?) ON CONFLICT(order_id) DO UPDATE SET {', '.join(f'{c}=excluded.{c}' for c in columns if c != 'order_id')}, processed_at=excluded.processed_at"
        now = datetime.now(timezone.utc).isoformat()
        with connect(self.path) as connection:
            for row in frame[columns].itertuples(index=False, name=None):
                values = tuple(value.item() if hasattr(value, "item") else value for value in row)
                values = tuple(value.isoformat() if hasattr(value, "isoformat") else value for value in values)
                connection.execute(sql, values + (now,))
        return len(frame)

    def save_run(self, run: dict[str, Any], analytics: dict[str, Any]) -> None:
        with connect(self.path) as connection:
            connection.execute("INSERT OR REPLACE INTO analytics_runs (run_id, started_at, completed_at, status, input_records, valid_records, invalid_records, duplicate_records, quality_report, reports) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (run["run_id"], run["started_at"], run.get("completed_at"), run["status"], run["input_records"], run["valid_records"], run["invalid_records"], run["duplicate_records"], json.dumps(run.get("quality", {})), json.dumps(run.get("reports", []))))
            now = datetime.now(timezone.utc).isoformat()
            for group, values in analytics.items():
                if isinstance(values, dict) and group in {"kpis", "trends", "comparison"}:
                    for name, value in values.items():
                        connection.execute("INSERT INTO analytics_snapshots (run_id, metric_name, metric_value, created_at) VALUES (?, ?, ?, ?)", (run["run_id"], f"{group}.{name}", json.dumps(value), now))

    def get_run(self, run_id: str) -> dict[str, Any] | None:
        with connect(self.path) as connection:
            row = connection.execute("SELECT * FROM analytics_runs WHERE run_id = ?", (run_id,)).fetchone()
        return self._run(row) if row else None

    def list_runs(self) -> list[dict[str, Any]]:
        with connect(self.path) as connection:
            rows = connection.execute("SELECT * FROM analytics_runs ORDER BY started_at DESC").fetchall()
        return [self._run(row) for row in rows]

    def list_records(self, limit=100, offset=0) -> list[dict[str, Any]]:
        with connect(self.path) as connection:
            rows = connection.execute("SELECT * FROM sales_records ORDER BY order_date DESC LIMIT ? OFFSET ?", (limit, offset)).fetchall()
        return [dict(row) for row in rows]

    def get_record(self, order_id: str) -> dict[str, Any] | None:
        with connect(self.path) as connection:
            row = connection.execute("SELECT * FROM sales_records WHERE order_id = ?", (order_id,)).fetchone()
        return dict(row) if row else None

    @staticmethod
    def _run(row: Any) -> dict[str, Any]:
        result = dict(row); result["quality"] = json.loads(result.pop("quality_report") or "{}"); result["reports"] = json.loads(result.pop("reports") or "[]"); return result
