from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from src.database.repository import NotificationRepository
from src.models.notification import Notification


class NotificationService:
    def __init__(self):
        self.repository = NotificationRepository()

    def create_notification(self, session: Session, payload: dict[str, Any]) -> Notification:
        return self.repository.create(session, payload)

    def list_notifications(self, session: Session) -> list[Notification]:
        return self.repository.list(session)
