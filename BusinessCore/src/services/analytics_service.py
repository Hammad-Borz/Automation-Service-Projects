from __future__ import annotations

from collections import Counter
from typing import Any

from sqlalchemy.orm import Session

from src.database.repository import count_rows
from src.models.customer import Customer
from src.models.notification import Notification
from src.models.order import Order
from src.models.task import Task


class AnalyticsService:
    def summarize(self, session: Session) -> dict[str, Any]:
        customers = session.query(Customer).all()
        orders = session.query(Order).all()
        tasks = session.query(Task).all()
        notifications = session.query(Notification).all()

        total_customers = len(customers)
        active_customers = sum(1 for c in customers if c.status == "active")
        total_orders = len(orders)
        completed_orders = sum(1 for o in orders if o.status == "completed")
        pending_orders = sum(1 for o in orders if o.status == "pending")
        cancelled_orders = sum(1 for o in orders if o.status == "cancelled")
        total_revenue = sum(float(o.total_amount or 0) for o in orders)
        total_quantity = sum(int(o.quantity or 0) for o in orders)
        average_order_value = (total_revenue / total_orders) if total_orders else 0.0

        orders_by_category = dict(sorted(Counter(o.category for o in orders).items()))
        orders_by_priority = dict(sorted(Counter(o.priority for o in orders).items()))
        orders_by_status = dict(sorted(Counter(o.status for o in orders).items()))
        orders_by_source = dict(sorted(Counter(o.source for o in orders).items()))

        tasks_created = len(tasks)
        completed_tasks = sum(1 for t in tasks if t.status == "completed")
        pending_tasks = sum(1 for t in tasks if t.status == "pending")
        notifications_generated = len(notifications)

        return {
            "total_customers": total_customers,
            "active_customers": active_customers,
            "total_orders": total_orders,
            "completed_orders": completed_orders,
            "pending_orders": pending_orders,
            "cancelled_orders": cancelled_orders,
            "total_revenue": round(total_revenue, 2),
            "average_order_value": round(average_order_value, 2),
            "total_quantity": total_quantity,
            "orders_by_category": orders_by_category,
            "orders_by_priority": orders_by_priority,
            "orders_by_status": orders_by_status,
            "orders_by_source": orders_by_source,
            "tasks_created": tasks_created,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "notifications_generated": notifications_generated,
        }
