import pytest

from src.result_validator import validate_assistant_response, validate_tool_result


def test_validates_successful_tool_result():
    assert validate_tool_result({"success": True, "operation": "list_tasks", "data": {"tasks": []}}).success


def test_rejects_inconsistent_tool_result():
    with pytest.raises(ValueError):
        validate_tool_result({"success": True, "operation": "list_tasks"})


def test_rejects_invalid_assistant_response():
    with pytest.raises(ValueError):
        validate_assistant_response({"request": "x", "mode": "demo", "message": "x", "tool_result": {"success": False, "operation": "x"}})
