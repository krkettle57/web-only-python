from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from yaoya.models.base import BaseDataModel
from yaoya.models.item import Item


@dataclass(frozen=True)
class OrderDetail(BaseDataModel):
    order_no: int
    item: Item
    quantity: int
    subtotal_price: int

    def to_dict(self) -> dict:
        return dict(
            order_no=self.order_no,
            item=self.item.to_dict(),
            quantity=self.quantity,
            subtotal_price=self.subtotal_price,
        )

    @classmethod
    def from_dict(cls, data: dict) -> OrderDetail:
        return OrderDetail(
            order_no=data["order_no"],
            item=Item.from_dict(data["item"]),
            quantity=data["quantity"],
            subtotal_price=data["subtotal_price"],
        )


@dataclass(frozen=True)
class Order(BaseDataModel):
    order_id: str
    user_id: str
    total_price: int
    ordered_at: datetime
    details: list[OrderDetail]

    def to_dict(self) -> dict:
        details = [detail.to_dict() for detail in self.details]
        return dict(
            order_id=self.order_id,
            user_id=self.user_id,
            total_price=self.total_price,
            ordered_at=self.ordered_at,
            details=details,
        )

    @classmethod
    def from_dict(cls, data: dict) -> Order:
        ordered_at = data["ordered_at"]
        if isinstance(ordered_at, str):
            ordered_at = datetime.fromisoformat(ordered_at)
        details = [OrderDetail.from_dict(detail_data) for detail_data in data["details"]]
        return Order(
            order_id=data["order_id"],
            user_id=data["user_id"],
            total_price=data["total_price"],
            ordered_at=ordered_at,
            details=details,
        )
