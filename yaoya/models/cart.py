from dataclasses import dataclass, field
from typing import List

from yaoya.models.item import Item


@dataclass
class CartItem:
    item_no: int
    item: Item
    quantity: int


@dataclass
class Cart:
    user_id: str
    cart_items: List[CartItem] = field(default_factory=list)

    def add_item(self, item: Item, quantity: int) -> None:
        cart_item = CartItem(
            item_no=len(self.cart_items) + 1,
            item=item,
            quantity=quantity,
        )
        self.cart_items.append(cart_item)

    def clear(self) -> None:
        self.cart_items = []
