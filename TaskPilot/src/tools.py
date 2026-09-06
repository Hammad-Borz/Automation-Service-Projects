"""Structured functions exposed to the assistant as business tools."""

from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from .models import TaskCreate, TaskUpdate, ToolResult
from .task_manager import TaskManager, TaskNotFoundError, TaskStorageError


def _task_data(task: Any) -> dict[str, Any]:
    return task.model_dump(mode="json")


def _failure(operation: str, error: Exception) -> ToolResult:
    return ToolResult(success=False, operation=operation, error=str(error))


def create_task_tool(manager: TaskManager, payload: dict[str, Any]) -> ToolResult:
    try:
        return ToolResult(success=True, operation="create_task", data={"task": _task_data(manager.create_task(TaskCreate.model_validate(payload)))})
    except (ValidationError, TaskStorageError) as error:
        return _failure("create_task", error)


def list_tasks_tool(manager: TaskManager, payload: dict[str, Any] | None = None) -> ToolResult:
    try:
        tasks = manager.list_tasks()
        return ToolResult(success=True, operation="list_tasks", data={"tasks": [_task_data(task) for task in tasks], "count": len(tasks)})
    except TaskStorageError as error:
        return _failure("list_tasks", error)


def update_task_tool(manager: TaskManager, payload: dict[str, Any]) -> ToolResult:
    try:
        task_id = str(payload.pop("task_id"))
        return ToolResult(success=True, operation="update_task", data={"task": _task_data(manager.update_task(task_id, TaskUpdate.model_validate(payload)))})
    except (KeyError, ValidationError, TaskNotFoundError, TaskStorageError) as error:
        return _failure("update_task", error)


def complete_task_tool(manager: TaskManager, payload: dict[str, Any]) -> ToolResult:
    try:
        return ToolResult(success=True, operation="complete_task", data={"task": _task_data(manager.complete_task(str(payload["task_id"])))})
    except (KeyError, TaskNotFoundError, TaskStorageError) as error:
        return _failure("complete_task", error)


def delete_task_tool(manager: TaskManager, payload: dict[str, Any]) -> ToolResult:
    try:
        return ToolResult(success=True, operation="delete_task", data={"task": _task_data(manager.delete_task(str(payload["task_id"])))})
    except (KeyError, TaskNotFoundError, TaskStorageError) as error:
        return _failure("delete_task", error)


def task_summary_tool(manager: TaskManager, payload: dict[str, Any] | None = None) -> ToolResult:
    try:
        return ToolResult(success=True, operation="task_summary", data={"summary": manager.get_task_summary().model_dump()})
    except TaskStorageError as error:
        return _failure("task_summary", error)


TOOL_DEFINITIONS = [
    {"type": "function", "function": {"name": "create_task", "description": "Create a business task.", "parameters": {"type": "object", "properties": {"title": {"type": "string"}, "description": {"type": "string"}, "priority": {"type": "string", "enum": ["low", "medium", "high"]}}, "required": ["title"]}}},
    {"type": "function", "function": {"name": "list_tasks", "description": "List all tasks.", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "update_task", "description": "Update a task.", "parameters": {"type": "object", "properties": {"task_id": {"type": "string"}, "title": {"type": "string"}, "description": {"type": "string"}, "priority": {"type": "string", "enum": ["low", "medium", "high"]}}, "required": ["task_id"]}}},
    {"type": "function", "function": {"name": "complete_task", "description": "Mark a task complete.", "parameters": {"type": "object", "properties": {"task_id": {"type": "string"}}, "required": ["task_id"]}}},
    {"type": "function", "function": {"name": "delete_task", "description": "Delete a task.", "parameters": {"type": "object", "properties": {"task_id": {"type": "string"}}, "required": ["task_id"]}}},
    {"type": "function", "function": {"name": "task_summary", "description": "Summarize task counts and priorities.", "parameters": {"type": "object", "properties": {}}}},
]


def execute_tool(manager: TaskManager, name: str, arguments: dict[str, Any]) -> ToolResult:
    handlers = {"create_task": create_task_tool, "list_tasks": list_tasks_tool, "update_task": update_task_tool, "complete_task": complete_task_tool, "delete_task": delete_task_tool, "task_summary": task_summary_tool}
    handler = handlers.get(name)
    if not handler:
        return ToolResult(success=False, operation=name or "unknown", error=f"Unknown tool: {name}")
    return handler(manager, dict(arguments))
