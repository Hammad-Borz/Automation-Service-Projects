from __future__ import annotations

import re
from typing import Any

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

REQUEST_ID_PATTERN = re.compile(r"^REQ-[A-Z0-9-]+$")


class CustomerInput(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    phone: str = Field(..., min_length=3)
    company: str = Field(..., min_length=1)

    @field_validator("name", "company")
    @classmethod
    def validate_non_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Field cannot be empty")
        return value.strip()


class OrderInput(BaseModel):
    product: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., ge=0)
    source: str = Field(..., min_length=1)

    @field_validator("product", "category", "source")
    @classmethod
    def validate_strings(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Field cannot be empty")
        return value.strip()

    @field_validator("unit_price")
    @classmethod
    def validate_positive_price(cls, value: float) -> float:
        if value < 0:
            raise ValueError("Price cannot be negative")
        return value

    @field_validator("quantity")
    @classmethod
    def validate_positive_quantity(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("Quantity must be positive")
        return value


class BusinessRequestInput(BaseModel):
    request_id: str
    customer: CustomerInput
    order: OrderInput

    @field_validator("request_id")
    @classmethod
    def validate_request_id_value(cls, value: str) -> str:
        return validate_request_id(value)


def validate_request_id(value: str) -> str:
    if not value or not value.strip():
        raise ValueError("Request ID is required")
    cleaned = value.strip()
    if not REQUEST_ID_PATTERN.match(cleaned):
        raise ValueError("Request ID must match format REQ-XXXX")
    return cleaned
