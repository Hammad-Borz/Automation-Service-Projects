import pytest

from src.core.action_registry import ActionRegistry, UnknownAutomationActionError


def test_registered_actions_are_available():
    actions = ActionRegistry.list_available()
    assert "create_task" in actions
    assert "generate_summary" in actions


def test_action_lookup_returns_callable():
    func = ActionRegistry.get("update_customer_status")
    assert callable(func)


def test_unknown_action_raises():
    with pytest.raises(UnknownAutomationActionError):
        ActionRegistry.get("not_real_action")


def test_registry_existence_check():
    assert ActionRegistry.exists("send_notification") is True
    assert ActionRegistry.exists("missing_action") is False
