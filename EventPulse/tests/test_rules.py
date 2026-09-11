from src.core.action_executor import execute_actions
from src.core.event_router import route_event
from src.core.rule_engine import evaluate_rules
from src.models.events import NormalizedEvent


def event(event_type, payload, source="website"):
    return NormalizedEvent("test", event_type, source, "2026-09-11T10:30:00+00:00", payload, "now")


def test_routes_known_and_unknown_events():
    assert route_event("order.created") == "order_automation"
    assert route_event("other") == "general_noop"


def test_high_value_order_rule():
    rules = evaluate_rules(event("order.created", {"total": 1500}), "order_automation")
    assert rules[0]["action"] == "flag_high_value_order"


def test_standard_order_does_not_flag():
    rules = evaluate_rules(event("order.created", {"total": 50}), "order_automation")
    assert rules[0]["action"] == "no_action"


def test_payment_rules_prepare_two_actions():
    rules = evaluate_rules(event("payment.received", {}), "payment_automation")
    results = execute_actions(rules)
    assert [item["action"] for item in results] == ["record_payment", "prepare_confirmation"]


def test_urgent_support_routes():
    rules = evaluate_rules(event("support.ticket_created", {"priority": "urgent"}), "support_automation")
    assert rules[0]["action"] == "route_support"
