"""Validated domain models used throughout the workflow."""

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class EmailCategory(str, Enum):
    URGENT = "urgent"
    SUPPORT = "support"
    SALES = "sales"
    NEWSLETTER = "newsletter"
    INVOICE = "invoice"
    GENERAL = "general"


class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class EmailMessage(BaseModel):
    """Normalized inbound email data."""

    model_config = ConfigDict(str_strip_whitespace=True)
    message_id: str = Field(min_length=1)
    sender: str = Field(min_length=3)
    recipient: str = Field(min_length=3)
    subject: str = "(no subject)"
    body: str = ""
    received_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("sender", "recipient")
    @classmethod
    def validate_address(cls, value: str) -> str:
        if "@" not in value or value.startswith("@") or value.endswith("@"):
            raise ValueError("must contain a valid email address")
        return value


class AutomationRule(BaseModel):
    """A configurable rule with optional matching criteria and actions."""

    name: str
    categories: set[EmailCategory] = set()
    minimum_priority: Priority | None = None
    sender_contains: str | None = None
    actions: list[str] = Field(default_factory=list)


class ActionResult(BaseModel):
    action: str
    status: str = "completed"
    detail: str = ""


class ProcessingResult(BaseModel):
    """Complete audit-friendly result of processing an email."""

    message_id: str
    category: EmailCategory
    priority: Priority
    actions: list[ActionResult] = Field(default_factory=list)
    suggested_response: str | None = None
    processed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = Field(default_factory=dict)
