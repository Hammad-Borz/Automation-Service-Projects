"""Validation boundary for untrusted AI responses."""

import json
from typing import Any

from pydantic import ValidationError

from .models import DocumentAnalysis


class ResultValidationError(Exception):
    """Raised when an AI result does not match the required schema."""


def validate_analysis(raw_result: str | dict[str, Any]) -> DocumentAnalysis:
    """Parse and validate a JSON object into a DocumentAnalysis."""
    try:
        payload = json.loads(raw_result) if isinstance(raw_result, str) else raw_result
    except json.JSONDecodeError as exc:
        raise ResultValidationError("AI response was not valid JSON.") from exc

    if not isinstance(payload, dict):
        raise ResultValidationError("AI response must be a JSON object.")
    try:
        return DocumentAnalysis.model_validate(payload)
    except ValidationError as exc:
        raise ResultValidationError(f"AI response failed validation: {exc}") from exc
