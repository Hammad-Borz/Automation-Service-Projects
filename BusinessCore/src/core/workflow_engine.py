from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from pydantic import ValidationError
from sqlalchemy.orm import Session

from src.database.connection import get_session_factory, initialize_database
from src.database.repository import WorkflowRepository
from src.models.customer import Customer
from src.models.order import Order
from src.models.task import Task
from src.services.audit_service import AuditService
from src.services.customer_service import CustomerService
from src.services.notification_service import NotificationService
from src.services.order_service import OrderService
from src.services.task_service import TaskService
from src.core.business_rules import evaluate_order_rules
from src.core.validation import BusinessRequestInput


class WorkflowEngine:
    def __init__(self):
        self.customer_service = CustomerService()
        self.order_service = OrderService()
        self.task_service = TaskService()
        self.notification_service = NotificationService()
        self.audit_service = AuditService()
        self.workflow_repository = WorkflowRepository()

    @staticmethod
    def _is_blocked_customer(customer_payload: Any) -> bool:
        if customer_payload is None:
            return False
        text = " ".join(
            [
                str(getattr(customer_payload, "name", "")),
                str(getattr(customer_payload, "email", "")),
                str(getattr(customer_payload, "company", "")),
            ]
        ).lower()
        return "blocked" in text

    def process_business_request(self, payload: dict[str, Any]) -> dict[str, Any]:
        try:
            request_data = BusinessRequestInput(**payload)
        except ValidationError as exc:
            return {
                "workflow_id": f"WF-INVALID-{uuid.uuid4().hex[:8].upper()}",
                "customer_id": None,
                "order_id": None,
                "order_status": "failed",
                "priority": "normal",
                "total_amount": 0.0,
                "created_task_ids": [],
                "notification_ids": [],
                "audit_event_ids": [],
                "success": False,
                "errors": exc.errors(),
                "idempotent": False,
            }

        initialize_database()
        with get_session_factory()() as session:
            existing = self.workflow_repository.get_by_request_id(session, request_data.request_id)
            if existing:
                self.audit_service.record_event(
                    session,
                    entity_type="workflow",
                    entity_id=existing.id,
                    event_type="DUPLICATE_REQUEST_DETECTED",
                    description="Duplicate request ID detected; returning existing workflow result.",
                    metadata={"request_id": request_data.request_id},
                )
                session.commit()
                return {
                    "workflow_id": existing.id,
                    "customer_id": existing.customer_id,
                    "order_id": existing.order_id,
                    "order_status": "pending" if existing.order_id is None else (existing.status or "processing"),
                    "priority": existing.priority,
                    "total_amount": existing.total_amount,
                    "created_task_ids": [],
                    "notification_ids": [],
                    "audit_event_ids": [],
                    "success": existing.success,
                    "errors": existing.errors,
                    "idempotent": True,
                }

            workflow_id = f"WF-{uuid.uuid4().hex[:8].upper()}"
            workflow = self.workflow_repository.create(
                session,
                {
                    "id": workflow_id,
                    "request_id": request_data.request_id,
                    "customer_id": None,
                    "order_id": None,
                    "status": "pending",
                    "priority": "normal",
                    "total_amount": 0.0,
                    "success": False,
                    "errors": None,
                    "workflow_data": {},
                },
            )

            try:
                customer = self.customer_service.find_by_email(session, request_data.customer.email)
                if not customer:
                    customer = self.customer_service.create_customer(
                        session,
                        {
                            "name": request_data.customer.name,
                            "email": request_data.customer.email.lower(),
                            "phone": request_data.customer.phone,
                            "company": request_data.customer.company,
                            "status": "active",
                        },
                    )
                    self.audit_service.record_event(
                        session,
                        entity_type="customer",
                        entity_id=customer.id,
                        event_type="CUSTOMER_CREATED",
                        description="Customer created during workflow processing.",
                        metadata={"email": customer.email},
                    )
                else:
                    self.audit_service.record_event(
                        session,
                        entity_type="customer",
                        entity_id=customer.id,
                        event_type="CUSTOMER_FOUND",
                        description="Existing customer matched during processing.",
                        metadata={"email": customer.email},
                    )

                blocked_customer = customer.status == "blocked" or self._is_blocked_customer(request_data.customer)
                if blocked_customer:
                    customer.status = "blocked"
                    workflow.customer_id = customer.id
                    workflow.status = "rejected"
                    workflow.success = False
                    workflow.errors = "Customer is blocked and the order was rejected"
                    self.audit_service.record_event(
                        session,
                        entity_type="order",
                        entity_id="N/A",
                        event_type="ORDER_REJECTED",
                        description="Order rejected because customer is blocked.",
                        metadata={"customer_id": customer.id, "request_id": request_data.request_id},
                    )
                    session.commit()
                    return {
                        "workflow_id": workflow.id,
                        "customer_id": customer.id,
                        "order_id": None,
                        "order_status": "cancelled",
                        "priority": "normal",
                        "total_amount": 0.0,
                        "created_task_ids": [],
                        "notification_ids": [],
                        "audit_event_ids": [],
                        "success": False,
                        "errors": [workflow.errors],
                        "idempotent": False,
                    }

                total_amount = request_data.order.quantity * request_data.order.unit_price
                order = self.order_service.create_order(
                    session,
                    {
                        "customer_id": customer.id,
                        "product": request_data.order.product,
                        "category": request_data.order.category,
                        "quantity": request_data.order.quantity,
                        "unit_price": request_data.order.unit_price,
                        "total_amount": total_amount,
                        "priority": "normal",
                        "status": "pending",
                        "source": request_data.order.source,
                    },
                )
                workflow.order_id = order.id
                workflow.total_amount = float(order.total_amount)
                self.audit_service.record_event(
                    session,
                    entity_type="order",
                    entity_id=order.id,
                    event_type="ORDER_CREATED",
                    description="Order created for customer.",
                    metadata={"product": order.product, "customer_id": customer.id},
                )

                rule_context = {
                    "amount": total_amount,
                    "quantity": request_data.order.quantity,
                    "priority": "normal",
                    "customer_status": customer.status,
                }
                rules = evaluate_order_rules(rule_context, customer)
                order.priority = rules["priority"]
                order.status = "processing"
                order.updated_at = datetime.now(timezone.utc)
                workflow.priority = rules["priority"]
                workflow.workflow_data["rules"] = rules
                session.commit()

                created_task_ids: list[int] = []
                for task_definition in rules["tasks"]:
                    task = self.task_service.create_task(
                        session,
                        {
                            "order_id": order.id,
                            "task_type": task_definition["task_type"],
                            "description": task_definition["description"],
                            "status": "pending",
                            "priority": task_definition["priority"],
                        },
                    )
                    created_task_ids.append(task.id)
                    self.audit_service.record_event(
                        session,
                        entity_type="task",
                        entity_id=task.id,
                        event_type="TASK_CREATED",
                        description=f"Generated task: {task.task_type}",
                        metadata={"order_id": order.id},
                    )

                notification_ids: list[int] = []
                for notification_definition in rules["notifications"]:
                    notification = self.notification_service.create_notification(
                        session,
                        {
                            "customer_id": customer.id,
                            "order_id": order.id,
                            "notification_type": notification_definition["notification_type"],
                            "recipient": customer.email,
                            "subject": notification_definition["subject"],
                            "message": notification_definition["message"],
                            "status": "generated",
                        },
                    )
                    notification_ids.append(notification.id)
                    self.audit_service.record_event(
                        session,
                        entity_type="notification",
                        entity_id=notification.id,
                        event_type="NOTIFICATION_GENERATED",
                        description=f"Generated notification: {notification.notification_type}",
                        metadata={"customer_id": customer.id},
                    )

                if created_task_ids:
                    for task in session.query(Task).filter(Task.id.in_(created_task_ids)).all():
                        task.status = "completed"
                        task.completed_at = datetime.now(timezone.utc)

                order.status = "completed"
                order.updated_at = datetime.now(timezone.utc)
                workflow.status = "completed"
                workflow.success = True
                workflow.customer_id = customer.id
                workflow.workflow_data["order"] = {"id": order.id, "total": order.total_amount}
                self.audit_service.record_event(
                    session,
                    entity_type="workflow",
                    entity_id=workflow.id,
                    event_type="WORKFLOW_COMPLETED",
                    description="Business workflow completed successfully.",
                    metadata={"request_id": request_data.request_id, "order_id": order.id},
                )
                session.commit()

                return {
                    "workflow_id": workflow.id,
                    "customer_id": customer.id,
                    "order_id": order.id,
                    "order_status": order.status,
                    "priority": rules["priority"],
                    "total_amount": float(order.total_amount),
                    "created_task_ids": created_task_ids,
                    "notification_ids": notification_ids,
                    "audit_event_ids": [],
                    "success": True,
                    "errors": [],
                    "idempotent": False,
                }
            except Exception as exc:
                workflow.status = "failed"
                workflow.success = False
                workflow.errors = str(exc)
                self.audit_service.record_event(
                    session,
                    entity_type="workflow",
                    entity_id=workflow.id,
                    event_type="WORKFLOW_FAILED",
                    description="Workflow failed during processing.",
                    metadata={"request_id": request_data.request_id, "error": str(exc)},
                )
                session.commit()
                return {
                    "workflow_id": workflow.id,
                    "customer_id": workflow.customer_id,
                    "order_id": workflow.order_id,
                    "order_status": "failed",
                    "priority": workflow.priority,
                    "total_amount": workflow.total_amount,
                    "created_task_ids": [],
                    "notification_ids": [],
                    "audit_event_ids": [],
                    "success": False,
                    "errors": [str(exc)],
                    "idempotent": False,
                }


def process_business_request(payload: dict[str, Any]) -> dict[str, Any]:
    return WorkflowEngine().process_business_request(payload)
