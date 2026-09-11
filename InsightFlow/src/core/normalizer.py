from typing import Any
import pandas as pd


def normalize_frame(frame: pd.DataFrame) -> pd.DataFrame:
    normalized = frame.copy()
    normalized.columns = [str(column).strip().lower() for column in normalized.columns]
    for column in normalized.columns:
        normalized[column] = normalized[column].map(_clean)
    for column in ("customer_name", "product", "category"):
        normalized[column] = normalized[column].map(lambda value: value.title() if isinstance(value, str) else value)
    for column in ("region",):
        normalized[column] = normalized[column].map(lambda value: value.title() if isinstance(value, str) else value)
    normalized["status"] = normalized["status"].map(lambda value: str(value).lower() if value else value)
    normalized["sales_channel"] = normalized["sales_channel"].map(lambda value: str(value).lower() if value else value)
    normalized["customer_email"] = normalized["customer_email"].map(lambda value: value.lower() if isinstance(value, str) else value)
    normalized["order_date"] = pd.to_datetime(normalized["order_date"], errors="coerce")
    normalized["quantity"] = pd.to_numeric(normalized["quantity"], errors="coerce")
    normalized["unit_price"] = pd.to_numeric(normalized["unit_price"], errors="coerce")
    normalized["total_amount"] = pd.to_numeric(normalized["total_amount"], errors="coerce")
    normalized["calculated_total"] = (normalized["quantity"] * normalized["unit_price"]).round(2)
    normalized["record_id"] = [str(value).strip() if value else f"row-{index + 1}" for index, value in enumerate(normalized.get("record_id", [None] * len(normalized)))]
    return normalized


def _clean(value: Any) -> Any:
    if pd.isna(value):
        return None
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return value
