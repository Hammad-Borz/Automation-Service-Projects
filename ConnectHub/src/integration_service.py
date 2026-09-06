"""Workflow orchestration for the ConnectHub integration."""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass
from typing import Any

from api_client import APIClient, APIClientError
from data_transformer import DataTransformer, TransformationError
from data_validator import DataValidator


@dataclass
class IntegrationSummary:
    total_fetched: int = 0
    valid_records: int = 0
    invalid_records: int = 0
    successfully_sent: int = 0
    failed_to_send: int = 0

    def to_dict(self) -> dict[str, int]:
        return asdict(self)


class IntegrationService:
    """Fetch, validate, transform, and send records between REST APIs."""

    def __init__(self, client: APIClient, validator: DataValidator | None = None, transformer: DataTransformer | None = None, logger: logging.Logger | None = None) -> None:
        self.client = client
        self.validator = validator or DataValidator()
        self.transformer = transformer or DataTransformer()
        self.logger = logger or logging.getLogger("connecthub")

    def run(self, source_url: str, destination_url: str) -> dict[str, int]:
        self.logger.info("Fetching source records from %s", source_url)
        source_data = self.client.get(source_url)
        batch = self.validator.validate_records(source_data)
        total_fetched = len(source_data) if isinstance(source_data, list) else 0
        summary = IntegrationSummary(total_fetched, len(batch.valid_records), len(batch.invalid_records))

        for invalid in batch.invalid_records:
            self.logger.warning("Skipping invalid record: %s", invalid.get("errors"))

        for record in batch.valid_records:
            try:
                payload = self.transformer.transform(record)
                self.client.post(destination_url, payload)
                summary.successfully_sent += 1
                self.logger.info("Sent record with id=%s", record["id"])
            except (APIClientError, TransformationError) as exc:
                summary.failed_to_send += 1
                self.logger.error("Could not send record with id=%s: %s", record.get("id", "unknown"), exc)

        self.logger.info("Integration completed: %s", summary.to_dict())
        return summary.to_dict()
