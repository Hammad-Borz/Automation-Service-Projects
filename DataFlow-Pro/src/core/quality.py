from collections import Counter
from typing import Any

import pandas as pd

from src.models.business import ValidationResult


def build_quality_report(input_count: int, results: list[ValidationResult], duplicate_count: int, cleaned_count: int) -> dict[str, Any]:
    errors = Counter(error for result in results for error in result.errors)
    valid_count = sum(result.valid for result in results)
    invalid_count = len(results) - valid_count
    score = round((valid_count / input_count) * 100, 2) if input_count else 100.0
    return {
        "input_records": input_count,
        "valid_records": valid_count,
        "invalid_records": invalid_count,
        "duplicate_records": duplicate_count,
        "cleaned_records": cleaned_count,
        "missing_values": sum(count for error, count in errors.items() if "required" in error),
        "invalid_emails": sum(count for error, count in errors.items() if "email" in error),
        "invalid_quantities": sum(count for error, count in errors.items() if "quantity" in error),
        "invalid_prices": sum(count for error, count in errors.items() if "unit_price" in error),
        "invalid_statuses": sum(count for error, count in errors.items() if "status" in error),
        "invalid_dates": sum(count for error, count in errors.items() if "order_date" in error),
        "validation_error_counts": dict(sorted(errors.items())),
        "quality_score": score,
    }


def detect_duplicates(frame: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    if frame.empty:
        return frame.copy(), 0
    duplicated = frame.duplicated("order_id", keep="first")
    return frame.loc[~duplicated].copy(), int(duplicated.sum())
