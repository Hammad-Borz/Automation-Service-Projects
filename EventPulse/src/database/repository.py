import json
import sqlite3
from typing import Any

from src.database.connection import connect
from src.models.events import NormalizedEvent, utc_now


class EventRepository:
    def __init__(self, database_path: str) -> None:
        self.database_path = database_path

    def create_event(self, event: NormalizedEvent) -> bool:
        try:
            with connect(self.database_path) as connection:
                connection.execute(
                    """
                    INSERT INTO events
                    (event_id, event_type, source, payload, received_at, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (event.event_id, event.event_type, event.source,
                     json.dumps(event.payload), event.received_at, "processing"),
                )
            return True
        except sqlite3.IntegrityError:
            self.record_duplicate(event.event_id)
            return False

    def record_duplicate(self, event_id: str) -> None:
        with connect(self.database_path) as connection:
            connection.execute(
                "INSERT INTO duplicate_events (event_id, detected_at) VALUES (?, ?)",
                (event_id, utc_now()),
            )

    def get_event(self, event_id: str) -> dict[str, Any] | None:
        with connect(self.database_path) as connection:
            row = connection.execute(
                "SELECT * FROM events WHERE event_id = ?", (event_id,)
            ).fetchone()
        return self._deserialize(row) if row else None

    def list_events(self, limit: int, offset: int) -> list[dict[str, Any]]:
        with connect(self.database_path) as connection:
            rows = connection.execute(
                "SELECT * FROM events ORDER BY received_at DESC LIMIT ? OFFSET ?",
                (limit, offset),
            ).fetchall()
        return [self._deserialize(row) for row in rows]

    def update_event(self, event_id: str, *, status: str, result: list[dict[str, Any]] | None = None,
                     error: str | None = None) -> None:
        with connect(self.database_path) as connection:
            connection.execute(
                """
                UPDATE events SET status = ?, processed_at = ?, result = ?, error = ?
                WHERE event_id = ?
                """,
                (status, utc_now(), json.dumps(result) if result is not None else None,
                 error, event_id),
            )

    def analytics(self) -> dict[str, Any]:
        with connect(self.database_path) as connection:
            total = connection.execute("SELECT COUNT(*) FROM events").fetchone()[0]
            completed = connection.execute(
                "SELECT COUNT(*) FROM events WHERE status = 'completed'"
            ).fetchone()[0]
            failed = connection.execute(
                "SELECT COUNT(*) FROM events WHERE status = 'failed'"
            ).fetchone()[0]
            duplicates = connection.execute("SELECT COUNT(*) FROM duplicate_events").fetchone()[0]
            by_type = connection.execute(
                "SELECT event_type, COUNT(*) AS count FROM events GROUP BY event_type"
            ).fetchall()
            action_rows = connection.execute(
                "SELECT result FROM events WHERE result IS NOT NULL"
            ).fetchall()
        actions = sum(len(json.loads(row[0])) for row in action_rows)
        return {
            "total_events": total,
            "completed_events": completed,
            "failed_events": failed,
            "duplicate_events": duplicates,
            "events_by_type": {row[0]: row[1] for row in by_type},
            "actions_prepared": actions,
        }

    @staticmethod
    def _deserialize(row: sqlite3.Row) -> dict[str, Any]:
        item = dict(row)
        item["payload"] = json.loads(item["payload"])
        item["result"] = json.loads(item["result"]) if item["result"] else []
        return item
