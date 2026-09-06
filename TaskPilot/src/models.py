"""Validated domain and response models for TaskPilot."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator, model_validator


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Status(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"


class Task(BaseModel):
    id: str = Field(default_factory=lambda: f"task_{uuid4().hex[:12]}")
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2_000)
    priority: Priority = Priority.MEDIUM
    status: Status = Status.PENDING
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    @field_validator("title")
    @classmethod
    def title_is_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("title must not be blank")
        return value


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2_000)
    priority: Priority = Priority.MEDIUM

    @field_validator("title")
    @classmethod
    def title_is_not_blank(cls, value: str) -> str:
        return Task.title_is_not_blank(value)


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2_000)
    priority: Priority | None = None

    @model_validator(mode="after")
    def has_changes(self) -> "TaskUpdate":
        if self.title is None and self.description is None and self.priority is None:
            raise ValueError("at least one field must be provided for an update")
        return self


class ToolResult(BaseModel):
    success: bool
    operation: str = Field(min_length=1)
    data: dict[str, Any] | None = None
    error: str | None = None

    @model_validator(mode="after")
    def is_consistent(self) -> "ToolResult":
        if self.success and self.error:
            raise ValueError("successful results cannot include an error")
        if not self.success and not self.error:
            raise ValueError("failed results must include an error message")
        return self


class AssistantResponse(BaseModel):
    request: str
    mode: str
    tool_result: ToolResult
    message: str


class TaskSummary(BaseModel):
    total_tasks: int
    pending_tasks: int
    completed_tasks: int
    priority_breakdown: dict[str, int]
