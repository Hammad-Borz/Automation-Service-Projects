from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from src.database.repository import AuditRepository
from src.models.audit import AuditEvent


class AuditService:
    def __init__(self):
        self.repository = AuditRepository()

    def record_event(
        self,
        session: Session,
        *,
        entity_type: str,
        entity_id: str | int,
        event_type: str,
        description: str,
        metadata: dict[str, Any] | None = None,
    ) -> AuditEvent:
        payload = {
            "entity_type": entity_type,
            "entity_id": str(entity_id),
            "event_type": event_type,
            "description": description,
            "event_data": metadata or {},
        }
        return self.repository.create(session, payload)

    def list_events(self, session: Session) -> list[AuditEvent]:
        return self.repository.list(session)
