from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


Status = Literal["pending", "completed", "cancelled", "refunded"]


class BusinessRecord(BaseModel):
    model_config = ConfigDict(extra="ignore")

    record_id: str
    order_id: str = Field(min_length=1)
    customer_name: str = Field(min_length=1)
    customer_email: str | None = None
    company: str | None = None
    product: str = Field(min_length=1)
    category: str = Field(min_length=1)
    quantity: int = Field(gt=0)
    unit_price: float = Field(ge=0)
    total_amount: float = Field(ge=0)
    currency: str = Field(min_length=3, max_length=3)
    order_date: date
    status: Status
    sales_region: str = Field(min_length=1)
    source: str
    is_high_value: bool
    processing_status: str = "valid"


class ValidationResult(BaseModel):
    record_id: str
    valid: bool
    errors: list[str] = Field(default_factory=list)
