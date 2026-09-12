from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.schemas import CustomerCreateRequest, OrderCreateRequest, WorkflowRequest
from src.core.validation import CustomerInput, OrderInput, validate_request_id
from src.core.workflow_engine import process_business_request
from src.database.connection import get_session_factory, initialize_database
from src.services.analytics_service import AnalyticsService
from src.services.audit_service import AuditService
from src.services.customer_service import CustomerService
from src.services.notification_service import NotificationService
from src.services.order_service import OrderService
from src.services.reporting_service import ReportingService
from src.services.task_service import TaskService

router = APIRouter(prefix="/api/v1")


def get_db() -> Session:
    initialize_database()
    db = get_session_factory()()
    try:
        yield db
    finally:
        db.close()


@router.post("/workflows/process")
def process_workflow(payload: WorkflowRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    try:
        response = process_business_request(payload.model_dump())
        return response
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Workflow processing failed.") from exc


@router.get("/workflows/{workflow_id}")
def get_workflow(workflow_id: str, db: Session = Depends(get_db)) -> dict[str, Any]:
    from src.database.repository import WorkflowRepository

    workflow = WorkflowRepository().get_by_id(db, workflow_id)
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return {
        "workflow_id": workflow.id,
        "request_id": workflow.request_id,
        "customer_id": workflow.customer_id,
        "order_id": workflow.order_id,
        "status": workflow.status,
        "priority": workflow.priority,
        "total_amount": workflow.total_amount,
        "success": workflow.success,
        "errors": workflow.errors,
    }


@router.post("/customers")
def create_customer(payload: CustomerCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    service = CustomerService()
    try:
        customer = service.create_customer(db, payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "id": customer.id,
        "name": customer.name,
        "email": customer.email,
        "phone": customer.phone,
        "company": customer.company,
        "status": customer.status,
    }


@router.get("/customers/{customer_id}")
def get_customer(customer_id: int, db: Session = Depends(get_db)) -> dict[str, Any]:
    customer = CustomerService().get_customer(db, customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {
        "id": customer.id,
        "name": customer.name,
        "email": customer.email,
        "phone": customer.phone,
        "company": customer.company,
        "status": customer.status,
    }


@router.get("/customers")
def list_customers(db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    customers = CustomerService().list_customers(db)
    return [{
        "id": c.id,
        "name": c.name,
        "email": c.email,
        "phone": c.phone,
        "company": c.company,
        "status": c.status,
    } for c in customers]


@router.post("/orders")
def create_order(payload: OrderCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    service = OrderService()
    order = service.create_order(db, payload.model_dump())
    return {
        "id": order.id,
        "customer_id": order.customer_id,
        "product": order.product,
        "category": order.category,
        "quantity": order.quantity,
        "unit_price": order.unit_price,
        "total_amount": order.total_amount,
        "priority": order.priority,
        "status": order.status,
    }


@router.get("/orders/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)) -> dict[str, Any]:
    order = OrderService().get_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return {
        "id": order.id,
        "customer_id": order.customer_id,
        "product": order.product,
        "category": order.category,
        "quantity": order.quantity,
        "unit_price": order.unit_price,
        "total_amount": order.total_amount,
        "priority": order.priority,
        "status": order.status,
        "source": order.source,
    }


@router.get("/orders")
def list_orders(db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    orders = OrderService().list_orders(db)
    return [{
        "id": o.id,
        "customer_id": o.customer_id,
        "product": o.product,
        "category": o.category,
        "quantity": o.quantity,
        "unit_price": o.unit_price,
        "total_amount": o.total_amount,
        "priority": o.priority,
        "status": o.status,
        "source": o.source,
    } for o in orders]


@router.get("/tasks")
def list_tasks(db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    tasks = TaskService().list_tasks(db)
    return [{
        "id": t.id,
        "order_id": t.order_id,
        "task_type": t.task_type,
        "description": t.description,
        "status": t.status,
        "priority": t.priority,
    } for t in tasks]


@router.get("/notifications")
def list_notifications(db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    notifications = NotificationService().list_notifications(db)
    return [{
        "id": n.id,
        "customer_id": n.customer_id,
        "order_id": n.order_id,
        "notification_type": n.notification_type,
        "recipient": n.recipient,
        "subject": n.subject,
        "message": n.message,
        "status": n.status,
    } for n in notifications]


@router.get("/audit")
def list_audit(db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    events = AuditService().list_events(db)
    return [{
        "id": e.id,
        "entity_type": e.entity_type,
        "entity_id": e.entity_id,
        "event_type": e.event_type,
        "description": e.description,
        "metadata": e.event_data,
    } for e in events]


@router.get("/analytics/summary")
def analytics_summary(db: Session = Depends(get_db)) -> dict[str, Any]:
    return AnalyticsService().summarize(db)


@router.post("/reports/generate")
def generate_report(db: Session = Depends(get_db)) -> dict[str, Any]:
    customers = CustomerService().list_customers(db)
    orders = OrderService().list_orders(db)
    tasks = TaskService().list_tasks(db)
    notifications = NotificationService().list_notifications(db)
    analytics = AnalyticsService().summarize(db)
    return ReportingService().build_report(analytics, customers, orders, tasks, notifications)


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "app": "BusinessCore", "environment": "development"}
