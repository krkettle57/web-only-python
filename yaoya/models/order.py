from __future__ import annotations

import json
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

    def to_dict(self) -> dict[str, str]:
        item_dict = self.item.to_dict()
        return dict(
            order_no=str(self.order_no),
            item=json.dumps(item_dict),
            quantity=str(self.quantity),
            subtotal_price=str(self.subtotal_price),
        )

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> OrderDetail:
        item_dict = json.loads(data["item"])
        return OrderDetail(
            order_no=int(data["order_no"]),
            item=Item.from_dict(item_dict),
            quantity=int(data["quantity"]),
            subtotal_price=int(data["subtotal_price"]),
        )


@dataclass(frozen=True)
class Order(BaseDataModel):
    order_id: str
    user_id: str
    total_price: int
    ordered_at: datetime
    details: list[OrderDetail]

    def to_dict(self) -> dict[str, str]:
        details = [detail.to_dict() for detail in self.details]
        return dict(
            order_id=self.order_id,
            user_id=self.user_id,
            total_price=str(self.total_price),
            ordered_at=self.ordered_at.isoformat(),
            details=json.dumps(details),
        )

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Order:
        details = [OrderDetail.from_dict(detail_dict) for detail_dict in json.loads(data["details"])]
        return Order(
            order_id=data["order_id"],
            user_id=data["user_id"],
            total_price=int(data["total_price"]),
            ordered_at=datetime.fromisoformat(data["ordered_at"]),
            details=details,
        )
