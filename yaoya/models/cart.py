from dataclasses import dataclass, field

from yaoya.models.item import Item


@dataclass
class CartItem:
    item_no: int
    item: Item
    quantity: int


@dataclass
class Cart:
    user_id: str
    cart_items: list[CartItem] = field(default_factory=list)
