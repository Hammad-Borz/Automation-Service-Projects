"""Validation for extracted product records."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


REQUIRED_FIELDS = ("name", "price", "category", "availability")


@dataclass(frozen=True)
class ValidationResult:
    is_valid: bool
    errors: tuple[str, ...] = ()


@dataclass(frozen=True)
class ValidationBatch:
    valid_records: list[dict[str, Any]]
    invalid_records: list[dict[str, Any]]


class DataValidator:
    """Validate records independently so valid items can continue."""

    def validate_record(self, record: Any) -> ValidationResult:
        if not isinstance(record, dict):
            return ValidationResult(False, ("Record must be a dictionary.",))
        errors: list[str] = []
        for field in REQUIRED_FIELDS:
            if field not in record:
                errors.append(f"Missing required field: {field}.")
            elif record[field] is None or (isinstance(record[field], str) and not record[field].strip()):
                errors.append(f"Required field cannot be empty: {field}.")
        return ValidationResult(not errors, tuple(errors))

    def validate_records(self, records: list[Any]) -> ValidationBatch:
        valid: list[dict[str, Any]] = []
        invalid: list[dict[str, Any]] = []
        for index, record in enumerate(records):
            result = self.validate_record(record)
            if result.is_valid:
                valid.append(record)
            else:
                invalid.append({"index": index, "record": record, "errors": list(result.errors)})
        return ValidationBatch(valid, invalid)
