import re
from typing import Any
import pandas as pd
from src.models.business import ValidationResult

STATUSES = {"completed", "pending", "cancelled", "refunded"}
CHANNELS = {"online", "retail", "marketplace"}
EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_frame(frame: pd.DataFrame) -> list[ValidationResult]:
    results = []
    for index, row in frame.iterrows():
        record_id = str(row.get("record_id") or f"row-{index + 1}")
        errors = []
        for field in ("order_id", "customer_id", "product"):
            if _blank(row.get(field)):
                errors.append(f"{field} is required")
        quantity = _number(row.get("quantity"))
        if quantity is None or quantity <= 0 or quantity != int(quantity):
            errors.append("quantity must be a positive integer")
        for field in ("unit_price", "total_amount"):
            value = _number(row.get(field))
            if value is None or value < 0:
                errors.append(f"{field} must be a non-negative number")
        email = _text(row.get("customer_email"))
        if email and not EMAIL.match(email):
            errors.append("customer_email is invalid")
        status = _text(row.get("status")).lower()
        if status not in STATUSES:
            errors.append("status is unsupported")
        channel = _text(row.get("sales_channel")).lower()
        if channel not in CHANNELS:
            errors.append("sales_channel is unsupported")
        if pd.isna(pd.to_datetime(row.get("order_date"), errors="coerce")):
            errors.append("order_date is invalid")
        if _blank(row.get("region")):
            errors.append("region is required")
        results.append(ValidationResult(record_id=record_id, valid=not errors, errors=errors))
    return results


def _text(value: Any) -> str:
    return "" if pd.isna(value) else str(value).strip()


def _blank(value: Any) -> bool:
    return not _text(value)


def _number(value: Any) -> float | None:
    try:
        if pd.isna(value) or str(value).strip() == "":
            return None
        return float(value)
    except (TypeError, ValueError):
        return None
