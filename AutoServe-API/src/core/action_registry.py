from __future__ import annotations

from collections.abc import Callable
from typing import Any, Final


class UnknownAutomationActionError(ValueError):
    """Raised when a requested automation type is not registered."""


ActionCallable = Callable[[dict[str, Any]], dict[str, Any]]


def send_notification(payload: dict[str, Any]) -> dict[str, Any]:
    recipient = payload.get("recipient")
    message = payload.get("message")
    return {
        "status": "simulated",
        "action": "send_notification",
        "recipient": recipient,
        "message": message,
        "result": "Notification simulated locally without external delivery.",
    }


def create_task(payload: dict[str, Any]) -> dict[str, Any]:
    title = payload.get("title")
    priority = payload.get("priority")
    return {
        "status": "simulated",
        "action": "create_task",
        "title": title,
        "priority": priority,
        "result": "Task created locally in the automation backend simulation.",
    }


def update_customer_status(payload: dict[str, Any]) -> dict[str, Any]:
    customer_id = payload.get("customer_id")
    status = payload.get("status")
    return {
        "status": "simulated",
        "action": "update_customer_status",
        "customer_id": customer_id,
        "updated_status": status,
        "result": "Customer status update simulated successfully.",
    }


def generate_summary(payload: dict[str, Any]) -> dict[str, Any]:
    text = payload.get("text")
    return {
        "status": "simulated",
        "action": "generate_summary",
        "summary": f"Summary generated from input: {text}",
        "result": "Summary generated locally without external services.",
    }


class ActionRegistry:
    """Map automation types to deterministic local simulation functions."""

    _actions: Final[dict[str, ActionCallable]] = {
        "send_notification": send_notification,
        "create_task": create_task,
        "update_customer_status": update_customer_status,
        "generate_summary": generate_summary,
    }

    @classmethod
    def register(cls, automation_type: str, handler: ActionCallable) -> None:
        cls._actions[automation_type] = handler

    @classmethod
    def get(cls, automation_type: str) -> ActionCallable:
        try:
            return cls._actions[automation_type]
        except KeyError as exc:
            raise UnknownAutomationActionError(
                f"Unknown automation action '{automation_type}'."
            ) from exc

    @classmethod
    def exists(cls, automation_type: str) -> bool:
        return automation_type in cls._actions

    @classmethod
    def list_available(cls) -> list[str]:
        return sorted(cls._actions)

    @classmethod
    def clear(cls) -> None:
        cls._actions.clear()
        cls._actions.update(
            {
                "send_notification": send_notification,
                "create_task": create_task,
                "update_customer_status": update_customer_status,
                "generate_summary": generate_summary,
            }
        )
