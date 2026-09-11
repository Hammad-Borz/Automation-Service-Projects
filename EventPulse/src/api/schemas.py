from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

SUPPORTED_EVENT_TYPES = {
    "lead.created", "lead.updated", "order.created", "payment.received",
    "support.ticket_created",
}


class WebhookEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_id: str = Field(min_length=1, max_length=200)
    event_type: str = Field(min_length=1, max_length=100)
    timestamp: datetime
    source: str = Field(min_length=1, max_length=100)
    data: dict[str, Any] = Field(default_factory=dict)

    @field_validator("event_type")
    @classmethod
    def validate_event_type(cls, value: str) -> str:
        if not value or any(char.isspace() for char in value):
            raise ValueError("event_type must be a non-empty identifier")
        return value


class ActionResult(BaseModel):
    action: str
    status: str
    message: str


class EventResponse(BaseModel):
    event_id: str
    status: str
    duplicate: bool = False
    result: list[ActionResult] = Field(default_factory=list)


class ErrorResponse(BaseModel):
    error: str
    detail: str


class RulesResponse(BaseModel):
    rules: list[dict[str, Any]]
