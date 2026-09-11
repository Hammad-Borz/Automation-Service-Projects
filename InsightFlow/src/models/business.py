from datetime import date
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


Status = Literal["completed", "pending", "cancelled", "refunded"]
Channel = Literal["online", "retail", "marketplace"]


class SalesRecord(BaseModel):
    model_config = ConfigDict(extra="ignore")
    record_id: str
    order_id: str = Field(min_length=1)
    customer_id: str = Field(min_length=1)
    customer_name: str = Field(min_length=1)
    customer_email: str | None = None
    product: str = Field(min_length=1)
    category: str = Field(min_length=1)
    quantity: int = Field(gt=0)
    unit_price: float = Field(ge=0)
    total_amount: float = Field(ge=0)
    calculated_total: float = Field(ge=0)
    order_date: date
    status: Status
    region: str = Field(min_length=1)
    sales_channel: Channel


class ValidationResult(BaseModel):
    record_id: str
    valid: bool
    errors: list[str] = Field(default_factory=list)
