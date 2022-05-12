from dataclasses import dataclass

from yaoya.models.item import Item


@dataclass(frozen=True)
class CartItem:
    item_no: int
    item: Item
    quantity: int


@dataclass(frozen=True)
class Cart:
    user_id: str
    cart_items: list[CartItem]
    total_price: int
