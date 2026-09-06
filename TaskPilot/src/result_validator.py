"""Boundary validation for tool and assistant responses."""

from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from .logger import get_logger
from .models import AssistantResponse, ToolResult


def validate_tool_result(value: ToolResult | dict[str, Any]) -> ToolResult:
    try:
        result = ToolResult.model_validate(value)
        if result.success and result.data is None:
            raise ValueError("successful tool results must include data")
        return result
    except (ValidationError, ValueError) as error:
        get_logger().warning("validation failure: %s", error)
        raise ValueError(f"Invalid tool result: {error}") from error


def validate_assistant_response(value: AssistantResponse | dict[str, Any]) -> AssistantResponse:
    try:
        response = AssistantResponse.model_validate(value)
        validate_tool_result(response.tool_result)
        return response
    except (ValidationError, ValueError) as error:
        get_logger().warning("assistant response validation failure: %s", error)
        raise ValueError(f"Invalid assistant response: {error}") from error
