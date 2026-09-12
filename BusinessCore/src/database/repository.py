from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.database.connection import Base
from src.models.audit import AuditEvent
from src.models.customer import Customer
from src.models.notification import Notification
from src.models.order import Order
from src.models.task import Task
from src.models.workflow import WorkflowExecution


class CustomerRepository:
    def create(self, session: Session, data: dict[str, Any]) -> Customer:
        customer = Customer(**data)
        session.add(customer)
        session.commit()
        session.refresh(customer)
        return customer

    def get_by_id(self, session: Session, customer_id: int) -> Customer | None:
        return session.query(Customer).filter(Customer.id == customer_id).first()

    def get_by_email(self, session: Session, email: str) -> Customer | None:
        return session.query(Customer).filter(Customer.email == email.lower()).first()

    def list(self, session: Session) -> list[Customer]:
        return session.query(Customer).order_by(Customer.created_at.desc()).all()


class OrderRepository:
    def create(self, session: Session, data: dict[str, Any]) -> Order:
        order = Order(**data)
        session.add(order)
        session.commit()
        session.refresh(order)
        return order

    def get_by_id(self, session: Session, order_id: int) -> Order | None:
        return session.query(Order).filter(Order.id == order_id).first()

    def list(self, session: Session) -> list[Order]:
        return session.query(Order).order_by(Order.created_at.desc()).all()

    def update(self, session: Session, order: Order, **kwargs: Any) -> Order:
        for key, value in kwargs.items():
            setattr(order, key, value)
        order.updated_at = datetime.now(timezone.utc)
        session.commit()
        session.refresh(order)
        return order


class TaskRepository:
    def create(self, session: Session, data: dict[str, Any]) -> Task:
        task = Task(**data)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    def list(self, session: Session) -> list[Task]:
        return session.query(Task).order_by(Task.created_at.desc()).all()

    def get_by_order(self, session: Session, order_id: int) -> list[Task]:
        return session.query(Task).filter(Task.order_id == order_id).all()


class NotificationRepository:
    def create(self, session: Session, data: dict[str, Any]) -> Notification:
        notification = Notification(**data)
        session.add(notification)
        session.commit()
        session.refresh(notification)
        return notification

    def list(self, session: Session) -> list[Notification]:
        return session.query(Notification).order_by(Notification.created_at.desc()).all()


class AuditRepository:
    def create(self, session: Session, data: dict[str, Any]) -> AuditEvent:
        event = AuditEvent(**data)
        session.add(event)
        session.commit()
        session.refresh(event)
        return event

    def list(self, session: Session) -> list[AuditEvent]:
        return session.query(AuditEvent).order_by(AuditEvent.created_at.desc()).all()


class WorkflowRepository:
    def create(self, session: Session, data: dict[str, Any]) -> WorkflowExecution:
        workflow = WorkflowExecution(**data)
        session.add(workflow)
        session.commit()
        session.refresh(workflow)
        return workflow

    def get_by_request_id(self, session: Session, request_id: str) -> WorkflowExecution | None:
        return session.query(WorkflowExecution).filter(WorkflowExecution.request_id == request_id).first()

    def get_by_id(self, session: Session, workflow_id: str) -> WorkflowExecution | None:
        return session.query(WorkflowExecution).filter(WorkflowExecution.id == workflow_id).first()

    def list(self, session: Session) -> list[WorkflowExecution]:
        return session.query(WorkflowExecution).order_by(WorkflowExecution.created_at.desc()).all()

    def update(self, session: Session, workflow: WorkflowExecution, **kwargs: Any) -> WorkflowExecution:
        for key, value in kwargs.items():
            setattr(workflow, key, value)
        workflow.updated_at = datetime.now(timezone.utc)
        session.commit()
        session.refresh(workflow)
        return workflow


def count_rows(session: Session, model: type) -> int:
    return session.query(func.count(model.id)).scalar() or 0
