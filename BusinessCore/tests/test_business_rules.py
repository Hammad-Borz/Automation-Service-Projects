from __future__ import annotations

from src.core.business_rules import evaluate_order_rules


def test_normal_order_rule():
    result = evaluate_order_rules({"customer_status": "active", "amount": 2500, "quantity": 2, "priority": "normal"}, None)
    assert result["priority"] == "normal"
    assert "prepare_invoice" in [item["task_type"] for item in result["tasks"]]


def test_high_value_order_rule():
    result = evaluate_order_rules({"customer_status": "active", "amount": 5000, "quantity": 3, "priority": "normal"}, None)
    assert result["priority"] == "high"
    assert any(item["task_type"] == "manager_approval" for item in result["tasks"])


def test_urgent_order_rule():
    result = evaluate_order_rules({"customer_status": "active", "amount": 12000, "quantity": 8, "priority": "normal"}, None)
    assert result["priority"] == "urgent"
    assert any(item["task_type"] == "manager_approval" for item in result["tasks"])


def test_bulk_quantity_rule():
    result = evaluate_order_rules({"customer_status": "active", "amount": 2000, "quantity": 12, "priority": "normal"}, None)
    assert any(item["task_type"] == "fulfillment" for item in result["tasks"])


def test_blocked_customer_rule():
    result = evaluate_order_rules({"customer_status": "blocked", "amount": 2000, "quantity": 2, "priority": "normal"}, None)
    assert result["blocked"] is True
    assert result["rejected"] is True
