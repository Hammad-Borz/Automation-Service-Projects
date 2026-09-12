from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from src.database.repository import CustomerRepository
from src.models.customer import Customer


class CustomerService:
    def __init__(self):
        self.repository = CustomerRepository()

    def create_customer(self, session: Session, payload: dict[str, Any]) -> Customer:
        normalized = payload.copy()
        normalized["email"] = str(normalized["email"]).lower().strip()
        existing = self.repository.get_by_email(session, normalized["email"])
        if existing is not None:
            return existing
        return self.repository.create(session, normalized)

    def get_customer(self, session: Session, customer_id: int) -> Customer | None:
        return self.repository.get_by_id(session, customer_id)

    def find_by_email(self, session: Session, email: str) -> Customer | None:
        return self.repository.get_by_email(session, email.lower().strip())

    def list_customers(self, session: Session) -> list[Customer]:
        return self.repository.list(session)
