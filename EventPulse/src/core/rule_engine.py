from typing import Any

from src.models.events import NormalizedEvent

SALES_TERMS = {"interested", "pricing", "quote", "demo", "buy"}


def evaluate_rules(event: NormalizedEvent, route: str) -> list[dict[str, Any]]:
    payload = event.payload
    if route in {"lead_automation", "lead_update_automation"}:
        message = str(payload.get("message", "")).lower()
        has_email = bool(payload.get("email"))
        source = str(payload.get("source", event.source)).lower()
        if has_email and source == "website":
            priority = "high" if SALES_TERMS.intersection(set(message.split())) else "medium"
            return [{"action": "notify_sales", "classification": "sales" if priority == "high" else "valid_lead", "priority": priority}]
        return [{"action": "no_action", "reason": "lead did not meet automation criteria"}]
    if route == "order_automation":
        total = float(payload.get("total", payload.get("amount", 0)) or 0)
        return [{"action": "flag_high_value_order" if total >= 1000 else "no_action", "order_total": total}]
    if route == "payment_automation":
        return [{"action": "record_payment"}, {"action": "prepare_confirmation"}]
    if route == "support_automation":
        action = "route_support" if str(payload.get("priority", "")).lower() in {"urgent", "high"} else "no_action"
        return [{"action": action, "priority": payload.get("priority", "standard")}]
    return [{"action": "no_action", "reason": "unknown event type"}]


def supported_rules() -> list[dict[str, Any]]:
    return [
        {"event_type": "lead.created", "condition": "website source and email", "action": "notify_sales"},
        {"event_type": "order.created", "condition": "total >= 1000", "action": "flag_high_value_order"},
        {"event_type": "payment.received", "condition": "any valid payment", "action": "record_payment and prepare_confirmation"},
        {"event_type": "support.ticket_created", "condition": "priority urgent or high", "action": "route_support"},
    ]
