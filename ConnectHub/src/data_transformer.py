"""Conversion from the source API schema to the destination schema."""

from __future__ import annotations

from typing import Any


class TransformationError(ValueError):
    """Raised when a record cannot be transformed."""


class DataTransformer:
    """Transform validated source records into destination payloads."""

    def transform(self, record: dict[str, Any]) -> dict[str, Any]:
        try:
            return {
                "external_id": record["id"],
                "full_name": record["name"],
                "contact_email": record["email"],
            }
        except KeyError as exc:
            raise TransformationError(f"Cannot transform record; missing field: {exc.args[0]}.") from exc
