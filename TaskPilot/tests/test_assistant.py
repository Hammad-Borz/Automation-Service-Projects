from src.assistant import TaskPilotAssistant


def test_demo_create_list_and_summary(manager):
    assistant = TaskPilotAssistant(manager, mode="demo")
    created = assistant.handle_request("Create a high priority task called Finish proposal")
    assert created.tool_result.success and created.tool_result.data["task"]["priority"] == "high"
    assert assistant.handle_request("List my tasks").tool_result.data["count"] == 1
    assert assistant.handle_request("Show my task summary").tool_result.operation == "task_summary"


def test_demo_complete_and_unknown_request(manager):
    assistant = TaskPilotAssistant(manager, mode="demo")
    task_id = assistant.handle_request("Create task called Call supplier").tool_result.data["task"]["id"]
    assert assistant.handle_request(f"Complete task {task_id}").tool_result.success
    assert not assistant.handle_request("Make the business better").tool_result.success


class MockProvider:
    def run(self, request, tools):
        assert any(tool["function"]["name"] == "create_task" for tool in tools)
        return "create_task", {"title": "From mock", "priority": "medium"}, "Mock selected a tool."


def test_openai_mode_is_mockable_without_network(manager):
    response = TaskPilotAssistant(manager, mode="openai", provider=MockProvider()).handle_request("Please add a task")
    assert response.mode == "openai" and response.tool_result.data["task"]["title"] == "From mock"
