from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from uuid import uuid4

JST = timezone(timedelta(hours=+9), "JST")


@dataclass
class OrderDetail:
    order_no: int
    item_id: str
    unit_price: int
    quantity: int
    subtotal_price: int


@dataclass
class Order:
    user_id: str
    order_id: str = field(default=str(uuid4()))
    total_price: int = field(default=0)
    ordered_at: datetime = field(default=datetime.now(JST))
    details: list[OrderDetail] = field(default_factory=list)

    def add_detail(self, item_id: str, unit_price: int, quantity: int) -> None:
        subtotal_price = unit_price * quantity
        order_detail = OrderDetail(
            order_no=len(self.details) + 1,
            item_id=item_id,
            unit_price=unit_price,
            quantity=quantity,
            subtotal_price=subtotal_price,
        )
        self.total_price += subtotal_price
        self.details.append(order_detail)
