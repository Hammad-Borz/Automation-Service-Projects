from typing import Any

import pandas as pd


def clean_dataframe(frame: pd.DataFrame, source: str) -> pd.DataFrame:
    cleaned = frame.copy()
    cleaned.columns = [str(column).strip().lower() for column in cleaned.columns]
    for column in cleaned.columns:
        cleaned[column] = cleaned[column].map(_clean_value)
    for column in ("customer_name", "product", "category"):
        if column in cleaned:
            cleaned[column] = cleaned[column].map(_title_case)
    if "customer_email" in cleaned:
        cleaned["customer_email"] = cleaned["customer_email"].map(lambda value: value.lower() if isinstance(value, str) else value)
    if "currency" not in cleaned:
        cleaned["currency"] = "USD"
    else:
        cleaned["currency"] = cleaned["currency"].map(lambda value: str(value).upper() if value else "USD")
    if "status" in cleaned:
        cleaned["status"] = cleaned["status"].map(lambda value: str(value).lower() if value else value)
    if "sales_region" in cleaned:
        cleaned["sales_region"] = cleaned["sales_region"].map(_title_case)
    cleaned["source"] = source
    cleaned["record_id"] = [str(value).strip() if value else f"row-{index + 1}" for index, value in enumerate(cleaned.get("record_id", [None] * len(cleaned)))]
    cleaned["order_date"] = pd.to_datetime(cleaned["order_date"], errors="coerce").dt.date
    return cleaned


def _clean_value(value: Any) -> Any:
    if pd.isna(value):
        return None
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return value


def _title_case(value: Any) -> Any:
    return value.title() if isinstance(value, str) else value
