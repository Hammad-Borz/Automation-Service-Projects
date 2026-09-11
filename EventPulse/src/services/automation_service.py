from typing import Any

from src.database.repository import EventRepository


def get_event_or_none(repository: EventRepository, event_id: str) -> dict[str, Any] | None:
    return repository.get_event(event_id)
