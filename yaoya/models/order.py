from datetime import datetime
from typing import NamedTuple

from yaoya.models.item import Item


class OrderDetail(NamedTuple):
    order_no: int
    item: Item
    quantity: int
    subtotal_price: int


class Order(NamedTuple):
    order_id: str
    user_id: str
    total_price: int
    ordered_at: datetime
    details: list[OrderDetail]
