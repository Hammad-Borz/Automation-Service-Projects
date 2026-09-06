import pytest

from src.task_manager import TaskManager


@pytest.fixture
def manager(tmp_path):
    return TaskManager(tmp_path / "tasks.json")
