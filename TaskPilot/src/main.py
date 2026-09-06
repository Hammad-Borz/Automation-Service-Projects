"""Command-line demo for TaskPilot."""

from __future__ import annotations

import argparse

from .assistant import TaskPilotAssistant
from .report_generator import generate_report
from .task_manager import TaskManager


def run_demo(manager: TaskManager) -> None:
    assistant = TaskPilotAssistant(manager, mode="demo")
    for request in ["Create a high priority task called Finish proposal", "Create a low priority task called Book team meeting", "List my tasks"]:
        response = assistant.handle_request(request)
        print(f"> {request}\n{response.message}: {response.tool_result.data or response.tool_result.error}\n")
    first = manager.list_tasks()[0]
    response = assistant.handle_request(f"Complete task {first.id}")
    print(f"> Complete task {first.id}\n{response.message}\n")
    print(f"> Show my task summary\n{assistant.handle_request('Show my task summary').tool_result.data}\n")
    print(f"Report generated: {generate_report(manager)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="TaskPilot — AI Business Assistant")
    parser.add_argument("--interactive", action="store_true", help="accept natural-language commands until 'quit'")
    args = parser.parse_args()
    manager = TaskManager()
    if not args.interactive:
        run_demo(manager)
        return
    assistant = TaskPilotAssistant(manager)
    print("TaskPilot interactive mode. Type 'quit' to exit.")
    while True:
        request = input("> ").strip()
        if request.lower() in {"quit", "exit"}:
            break
        response = assistant.handle_request(request)
        print(response.message, response.tool_result.model_dump(mode="json"))


if __name__ == "__main__":
    main()
