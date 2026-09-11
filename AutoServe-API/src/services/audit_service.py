from __future__ import annotations

from typing import Any

from src.database.repository import AutomationRepository
from src.models.automation import AuditLog, AuditEvent


class AuditService:
    def __init__(self, repository: AutomationRepository):
        self.repository = repository

    def record_event(
        self,
        *,
        job_id: str | None,
        run_id: str | None,
        event_type: AuditEvent | str,
        message: str,
        metadata: dict[str, Any] | None = None,
    ) -> AuditLog:
        event_name = event_type.value if isinstance(event_type, AuditEvent) else event_type
        log = AuditLog(
            id=f"AUD-{job_id or run_id or 'global'}-{len(self.repository.list_audit_logs(job_id=job_id, run_id=run_id)) + 1}",
            job_id=job_id,
            run_id=run_id,
            event_type=event_name,
            message=message,
            metadata=metadata or {},
        )
        return self.repository.create_audit_log(log)

    def list_logs(self, job_id: str | None = None, run_id: str | None = None) -> list[AuditLog]:
        return self.repository.list_audit_logs(job_id=job_id, run_id=run_id)
