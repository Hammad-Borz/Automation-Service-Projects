import pytest

from src.models import Priority, Status, TaskCreate, TaskUpdate
from src.task_manager import TaskNotFoundError


def test_create_persists_a_task(manager):
    task = manager.create_task(TaskCreate(title="Proposal", priority=Priority.HIGH))
    assert task.id.startswith("task_") and manager.list_tasks()[0].title == "Proposal"


def test_update_task(manager):
    task = manager.create_task(TaskCreate(title="Draft"))
    updated = manager.update_task(task.id, TaskUpdate(title="Final draft", priority=Priority.LOW))
    assert updated.title == "Final draft" and updated.priority == Priority.LOW


def test_complete_task(manager):
    task = manager.create_task(TaskCreate(title="Call client"))
    assert manager.complete_task(task.id).status == Status.COMPLETED


def test_delete_task(manager):
    task = manager.create_task(TaskCreate(title="Remove me"))
    assert manager.delete_task(task.id).id == task.id and manager.list_tasks() == []


def test_missing_task_is_safe(manager):
    with pytest.raises(TaskNotFoundError):
        manager.complete_task("task_missing")


def test_summary_calculations(manager):
    high = manager.create_task(TaskCreate(title="Urgent", priority=Priority.HIGH))
    manager.create_task(TaskCreate(title="Routine", priority=Priority.LOW))
    manager.complete_task(high.id)
    summary = manager.get_task_summary()
    assert (summary.total_tasks, summary.pending_tasks, summary.completed_tasks) == (2, 1, 1)
    assert summary.priority_breakdown["high"] == 1
