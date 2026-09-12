from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from src.database.repository import OrderRepository
from src.models.order import Order


class OrderService:
    def __init__(self):
        self.repository = OrderRepository()

    def create_order(self, session: Session, payload: dict[str, Any]) -> Order:
        order_data = payload.copy()
        if "total_amount" not in order_data:
            order_data["total_amount"] = float(order_data["quantity"]) * float(order_data["unit_price"])
        order_data["total_amount"] = float(order_data["total_amount"])
        return self.repository.create(session, order_data)

    def get_order(self, session: Session, order_id: int) -> Order | None:
        return self.repository.get_by_id(session, order_id)

    def list_orders(self, session: Session) -> list[Order]:
        return self.repository.list(session)

    def update_order(self, session: Session, order: Order, **kwargs: Any) -> Order:
        return self.repository.update(session, order, **kwargs)
