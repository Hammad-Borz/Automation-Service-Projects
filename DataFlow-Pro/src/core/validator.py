import re
from typing import Any

import pandas as pd

from src.models.business import ValidationResult

REQUIRED_COLUMNS = {"order_id", "customer_name", "product", "category", "quantity", "unit_price", "order_date", "status", "sales_region"}
VALID_STATUSES = {"pending", "completed", "cancelled", "refunded"}
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_columns(columns: list[str]) -> list[str]:
    return sorted(REQUIRED_COLUMNS - set(columns))


def validate_dataframe(frame: pd.DataFrame) -> list[ValidationResult]:
    results: list[ValidationResult] = []
    for index, row in frame.iterrows():
        record_id = str(row.get("record_id") or f"row-{index + 1}")
        errors: list[str] = []
        for field in REQUIRED_COLUMNS:
            if pd.isna(row.get(field)) or str(row.get(field)).strip() == "":
                errors.append(f"{field} is required")
        quantity = _number(row.get("quantity"))
        if quantity is None or quantity <= 0 or quantity != int(quantity):
            errors.append("quantity must be a positive integer")
        price = _number(row.get("unit_price"))
        if price is None or price < 0:
            errors.append("unit_price must be a non-negative number")
        email = _text(row.get("customer_email"))
        if email and not EMAIL_PATTERN.match(email):
            errors.append("customer_email is invalid")
        status = _text(row.get("status")).lower()
        if status and status not in VALID_STATUSES:
            errors.append("status is unsupported")
        parsed_date = pd.to_datetime(row.get("order_date"), errors="coerce")
        if pd.isna(parsed_date):
            errors.append("order_date is invalid")
        results.append(ValidationResult(record_id=record_id, valid=not errors, errors=errors))
    return results


def _number(value: Any) -> float | None:
    try:
        if pd.isna(value) or str(value).strip() == "":
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _text(value: Any) -> str:
    return "" if pd.isna(value) else str(value).strip()
