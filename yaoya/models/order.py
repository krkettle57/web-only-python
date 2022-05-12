from dataclasses import dataclass
from datetime import datetime

from yaoya.models.item import Item


@dataclass(frozen=True)
class OrderDetail:
    order_no: int
    item: Item
    quantity: int
    subtotal_price: int


@dataclass(frozen=True)
class Order:
    order_id: str
    user_id: str
    total_price: int
    ordered_at: datetime
    details: list[OrderDetail]
