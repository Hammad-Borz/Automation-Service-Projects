from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from src.core.validation import CustomerInput, OrderInput


class CustomerCreateRequest(BaseModel):
    name: str = Field(..., min_length=1)
    email: str
    phone: str = Field(..., min_length=3)
    company: str = Field(..., min_length=1)


class OrderCreateRequest(BaseModel):
    customer_id: int
    product: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., ge=0)
    source: str = Field(..., min_length=1)


class WorkflowRequest(BaseModel):
    request_id: str
    customer: CustomerInput
    order: OrderInput


class WorkflowResponse(BaseModel):
    workflow_id: str
    customer_id: int | None = None
    order_id: int | None = None
    order_status: str
    priority: str
    total_amount: float
    created_task_ids: list[int] = []
    notification_ids: list[int] = []
    audit_event_ids: list[int] = []
    success: bool
    errors: list[str] = []
    idempotent: bool = False


class HealthResponse(BaseModel):
    status: str
    app: str
    environment: str
