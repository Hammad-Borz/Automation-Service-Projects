"""Validation primitives for source API records."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


REQUIRED_FIELDS = ("id", "name", "email")


@dataclass(frozen=True)
class ValidationResult:
    is_valid: bool
    errors: tuple[str, ...] = ()


@dataclass(frozen=True)
class ValidationBatch:
    valid_records: list[dict[str, Any]]
    invalid_records: list[dict[str, Any]]


class DataValidator:
    """Validate source data while retaining valid records for processing."""

    def validate_records(self, records: Any) -> ValidationBatch:
        if not isinstance(records, list):
            return ValidationBatch([], [{"record": records, "errors": ["Source data must be a list of dictionaries."]}])

        valid_records: list[dict[str, Any]] = []
        invalid_records: list[dict[str, Any]] = []
        for index, record in enumerate(records):
            result = self.validate_record(record)
            if result.is_valid:
                valid_records.append(record)
            else:
                invalid_records.append({"index": index, "record": record, "errors": list(result.errors)})
        return ValidationBatch(valid_records, invalid_records)

    def validate_record(self, record: Any) -> ValidationResult:
        if not isinstance(record, dict):
            return ValidationResult(False, ("Record must be a dictionary.",))

        errors: list[str] = []
        for field in REQUIRED_FIELDS:
            if field not in record:
                errors.append(f"Missing required field: {field}.")
            elif record[field] is None or (isinstance(record[field], str) and not record[field].strip()):
                errors.append(f"Required field cannot be empty: {field}.")

        email = record.get("email")
        if email is not None and (not isinstance(email, str) or "@" not in email or email.startswith("@") or email.endswith("@")):
            errors.append("Email must be a valid email address.")
        return ValidationResult(not errors, tuple(errors))
