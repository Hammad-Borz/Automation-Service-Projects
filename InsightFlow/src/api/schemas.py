from pydantic import BaseModel, Field


class AnalyticsRunRequest(BaseModel):
    input_path: str | None = Field(default=None, max_length=500)


class AnalyticsRunResponse(BaseModel):
    run_id: str
    status: str
    input_records: int
    valid_records: int
    invalid_records: int
    duplicate_records: int
    reports: list[str] = []


class KPIResponse(BaseModel):
    model_config = {"extra": "allow"}


class TrendResponse(BaseModel):
    model_config = {"extra": "allow"}


class ComparisonResponse(BaseModel):
    model_config = {"extra": "allow"}


class CategoryResponse(BaseModel):
    model_config = {"extra": "allow"}


class ProductResponse(BaseModel):
    model_config = {"extra": "allow"}


class RegionResponse(BaseModel):
    model_config = {"extra": "allow"}


class ChannelResponse(BaseModel):
    model_config = {"extra": "allow"}


class CustomerSegmentResponse(BaseModel):
    model_config = {"extra": "allow"}


class AnomalyResponse(BaseModel):
    model_config = {"extra": "allow"}


class InsightResponse(BaseModel):
    model_config = {"extra": "allow"}


class DataQualityResponse(BaseModel):
    model_config = {"extra": "allow"}


class AnalyticsRunSummary(BaseModel):
    model_config = {"extra": "allow"}
