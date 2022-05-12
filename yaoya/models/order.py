from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from yaoya.models.item import Item


@dataclass(frozen=True)
class OrderDetail:
    order_no: int
    item: Item
    quantity: int
    subtotal_price: int

    @classmethod
    def from_dict(cls, data: dict) -> OrderDetail:
        return OrderDetail(
            order_no=data["order_no"],
            item=data["item"],
            quantity=data["quantity"],
            subtotal_price=data["subtotal_price"],
        )


@dataclass(frozen=True)
class Order:
    order_id: str
    user_id: str
    total_price: int
    ordered_at: datetime
    details: list[OrderDetail]

    @classmethod
    def from_dict(cls, data: dict) -> Order:
        return Order(
            order_id=data["order_id"],
            user_id=data["user_id"],
            total_price=data["total_price"],
            ordered_at=data["ordered_at"],
            details=data["details"],
        )
