import logging
from typing import Any

from src.core.action_executor import execute_actions
from src.core.event_router import route_event
from src.core.rule_engine import evaluate_rules
from src.database.repository import EventRepository
from src.models.events import NormalizedEvent

logger = logging.getLogger(__name__)


class EventProcessor:
    def __init__(self, repository: EventRepository) -> None:
        self.repository = repository

    def process(self, event: NormalizedEvent) -> dict[str, Any]:
        logger.info("Webhook received: %s", event.event_id)
        if not self.repository.create_event(event):
            logger.info("Duplicate detected: %s", event.event_id)
            return {"event_id": event.event_id, "status": "duplicate", "duplicate": True, "result": []}
        try:
            route = route_event(event.event_type)
            rules = evaluate_rules(event, route)
            actions = execute_actions(rules)
            self.repository.update_event(event.event_id, status="completed", result=actions)
            logger.info("Event completed: %s", event.event_id)
            return {"event_id": event.event_id, "status": "completed", "duplicate": False, "result": actions}
        except Exception as exc:
            logger.exception("Processing failure: %s", event.event_id)
            self.repository.update_event(event.event_id, status="failed", error=str(exc))
            raise
