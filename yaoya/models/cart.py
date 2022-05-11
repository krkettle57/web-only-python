from typing import NamedTuple

from yaoya.models.item import Item


class CartItem(NamedTuple):
    item_no: int
    item: Item
    quantity: int


class Cart(NamedTuple):
    user_id: str
    cart_items: list[CartItem]
    total_price: int
