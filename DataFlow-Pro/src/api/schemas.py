from typing import Any

from pydantic import BaseModel, Field


class PipelineRunRequest(BaseModel):
    input_path: str | None = Field(default=None, max_length=500)


class PipelineRunResponse(BaseModel):
    run_id: str
    status: str
    input_records: int
    valid_records: int
    invalid_records: int
    duplicate_records: int
    reports_generated: list[str] = Field(default_factory=list)


class PipelineRunSummary(BaseModel):
    run_id: str
    started_at: str
    completed_at: str | None = None
    status: str
    input_records: int
    valid_records: int
    invalid_records: int
    duplicate_records: int


class AnalyticsOverview(BaseModel):
    total_revenue: float
    total_orders: int
    total_quantity: int
    average_order_value: float
    completed_revenue: float
    cancelled_order_count: int
    refunded_order_count: int
    high_value_order_count: int
    revenue_by_category: dict[str, float]
    revenue_by_region: dict[str, float]
    revenue_by_product: dict[str, float]
    orders_by_status: dict[str, int]
    monthly_revenue: dict[str, float]


class QualityReport(BaseModel):
    input_records: int
    valid_records: int
    invalid_records: int
    duplicate_records: int
    quality_score: float


class BusinessRecordResponse(BaseModel):
    model_config = {"extra": "allow"}

    order_id: str
    customer_name: str
    product: str
    category: str
    quantity: int
    unit_price: float
    total_amount: float
    status: str
