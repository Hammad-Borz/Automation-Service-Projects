from __future__ import annotations

from typing import Any


def evaluate_order_rules(order_context: dict[str, Any], customer: Any) -> dict[str, Any]:
    amount = float(order_context.get("amount", 0))
    quantity = int(order_context.get("quantity", 0))
    priority = str(order_context.get("priority", "normal")).lower()
    customer_status = str((customer.status if customer else order_context.get("customer_status", "active"))).lower()

    tasks: list[dict[str, Any]] = []
    notifications: list[dict[str, Any]] = []
    blocked = customer_status == "blocked"
    rejected = False
    message = ""

    if blocked:
        rejected = True
        message = "Customer is blocked; order rejected"

    if amount >= 10000:
        priority = "urgent"
        tasks.append({"task_type": "manager_approval", "description": "Urgent order requires executive approval", "priority": "urgent"})
        tasks.append({"task_type": "review_order", "description": "High-value order requires additional review", "priority": "high"})
    elif amount >= 5000:
        priority = "high"
        tasks.append({"task_type": "manager_approval", "description": "High-value order requires manager approval", "priority": "high"})

    if quantity >= 10:
        tasks.append({"task_type": "fulfillment", "description": "Bulk order requires fulfillment coordination", "priority": "high"})

    tasks.append({"task_type": "prepare_invoice", "description": "Prepare invoice for the customer", "priority": "normal"})
    tasks.append({"task_type": "notify_customer", "description": "Notify customer about order progress", "priority": "normal"})

    if priority in {"high", "urgent"}:
        notifications.append({
            "notification_type": "priority_order",
            "subject": "Priority Order Review",
            "message": "Your order has been flagged for priority processing.",
        })

    if not blocked:
        notifications.append({
            "notification_type": "order_confirmation",
            "subject": "Order Confirmation",
            "message": "Your order has been received and is being processed.",
        })

    return {
        "priority": priority,
        "tasks": tasks,
        "notifications": notifications,
        "blocked": blocked,
        "rejected": rejected,
        "message": message,
    }
