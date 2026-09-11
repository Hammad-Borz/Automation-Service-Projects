from __future__ import annotations

from src.database.repository import AutomationRepository


class MetricsService:
    def __init__(self, repository: AutomationRepository):
        self.repository = repository

    def get_summary(self) -> dict[str, float | int]:
        return self.repository.metrics_summary()
