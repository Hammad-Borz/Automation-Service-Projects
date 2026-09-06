"""Intent routing for offline demo and OpenAI function-calling modes."""

from __future__ import annotations

import json
import os
import re
from typing import Any, Protocol

from .logger import get_logger
from .models import AssistantResponse, ToolResult
from .result_validator import validate_assistant_response, validate_tool_result
from .task_manager import TaskManager
from .tools import TOOL_DEFINITIONS, execute_tool


class ToolCallingProvider(Protocol):
    def run(self, request: str, tools: list[dict[str, Any]]) -> tuple[str, dict[str, Any], str]: ...


class OpenAIProvider:
    """Small adapter that asks OpenAI for a tool call; imported only when used."""

    def __init__(self, api_key: str, model: str = "gpt-4o-mini") -> None:
        self.api_key, self.model = api_key, model

    def run(self, request: str, tools: list[dict[str, Any]]) -> tuple[str, dict[str, Any], str]:
        from openai import OpenAI  # Optional dependency in demo mode.

        client = OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": "You are a task assistant. Use a supplied tool."}, {"role": "user", "content": request}],
            tools=tools,
            tool_choice="required",
        )
        call = response.choices[0].message.tool_calls[0]
        return call.function.name, json.loads(call.function.arguments or "{}"), "Tool selected by OpenAI."


class TaskPilotAssistant:
    def __init__(self, manager: TaskManager, mode: str | None = None, provider: ToolCallingProvider | None = None) -> None:
        self.manager = manager
        self.mode = (mode or os.getenv("TASKPILOT_MODE", "demo")).lower()
        self.provider = provider
        self.logger = get_logger()

    def handle_request(self, request: str) -> AssistantResponse:
        if self.mode == "openai" and (self.provider or os.getenv("OPENAI_API_KEY")):
            return self._handle_openai(request)
        return self._handle_demo(request)

    def _response(self, request: str, mode: str, result: ToolResult, message: str) -> AssistantResponse:
        response = AssistantResponse(request=request, mode=mode, tool_result=validate_tool_result(result), message=message)
        return validate_assistant_response(response)

    def _handle_demo(self, request: str) -> AssistantResponse:
        text = request.strip()
        lowered = text.lower()
        name, arguments = "", {}
        create = re.match(r"(?:create|add)\s+(?:a\s+)?(?:(low|medium|high)\s+priority\s+)?task\s+(?:called\s+)?(.+)", text, re.I)
        update = re.match(r"update\s+task\s+(\S+)\s+(?:title\s+to\s+)?(.+)", text, re.I)
        identifier = re.search(r"(?:complete|delete)\s+task\s+(\S+)", text, re.I)
        if create:
            name, arguments = "create_task", {"title": create.group(2).strip(), "priority": (create.group(1) or "medium").lower()}
        elif lowered.startswith(("list", "show")) and "task" in lowered and "summary" not in lowered:
            name = "list_tasks"
        elif update:
            name, arguments = "update_task", {"task_id": update.group(1), "title": update.group(2).strip()}
        elif identifier and lowered.startswith("complete"):
            name, arguments = "complete_task", {"task_id": identifier.group(1)}
        elif identifier and lowered.startswith("delete"):
            name, arguments = "delete_task", {"task_id": identifier.group(1)}
        elif "summary" in lowered:
            name = "task_summary"
        else:
            result = ToolResult(success=False, operation="interpret_request", error="I could not determine a supported task action.")
            return self._response(text, "demo", result, "Try creating, listing, updating, completing, deleting, or summarizing tasks.")
        self.logger.info("assistant selected tool: %s", name)
        result = execute_tool(self.manager, name, arguments)
        message = "Request completed." if result.success else f"Request failed: {result.error}"
        return self._response(text, "demo", result, message)

    def _handle_openai(self, request: str) -> AssistantResponse:
        try:
            provider = self.provider or OpenAIProvider(os.environ["OPENAI_API_KEY"], os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
            name, arguments, message = provider.run(request, TOOL_DEFINITIONS)
            self.logger.info("assistant selected tool: %s", name)
            result = execute_tool(self.manager, name, arguments)
            return self._response(request, "openai", result, message if result.success else f"{message} {result.error}")
        except Exception as error:  # Network/provider errors become a safe structured response.
            self.logger.exception("unexpected OpenAI assistant error")
            return self._response(request, "openai", ToolResult(success=False, operation="openai_tool_call", error=str(error)), "OpenAI tool-calling request failed.")
