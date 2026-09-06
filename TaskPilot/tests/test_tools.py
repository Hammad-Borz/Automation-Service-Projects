from src.tools import complete_task_tool, create_task_tool, delete_task_tool, list_tasks_tool, task_summary_tool, update_task_tool


def test_create_and_list_tools(manager):
    created = create_task_tool(manager, {"title": "Send invoice", "priority": "high"})
    listed = list_tasks_tool(manager)
    assert created.success and listed.data["count"] == 1


def test_update_complete_delete_tools(manager):
    task = create_task_tool(manager, {"title": "Draft brief"}).data["task"]
    assert update_task_tool(manager, {"task_id": task["id"], "title": "Final brief"}).success
    assert complete_task_tool(manager, {"task_id": task["id"]}).data["task"]["status"] == "completed"
    assert delete_task_tool(manager, {"task_id": task["id"]}).success


def test_tool_returns_structured_missing_error(manager):
    result = complete_task_tool(manager, {"task_id": "unknown"})
    assert not result.success and result.operation == "complete_task" and result.error


def test_summary_tool(manager):
    create_task_tool(manager, {"title": "One"})
    assert task_summary_tool(manager).data["summary"]["total_tasks"] == 1
