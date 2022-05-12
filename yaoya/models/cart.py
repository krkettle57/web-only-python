from __future__ import annotations

from dataclasses import dataclass

from yaoya.models.item import Item


@dataclass(frozen=True)
class CartItem:
    item_no: int
    item: Item
    quantity: int

    @classmethod
    def from_dict(cls, data: dict) -> CartItem:
        return CartItem(
            item_no=data["item_no"],
            item=data["item"],
            quantity=data["quantity"],
        )


@dataclass(frozen=True)
class Cart:
    user_id: str
    cart_items: list[CartItem]
    total_price: int

    @classmethod
    def from_dict(cls, data: dict) -> Cart:
        cart_items = [CartItem.from_dict(cart_item_data) for cart_item_data in data["cart_items"]]
        return Cart(
            user_id=data["user_id"],
            cart_items=cart_items,
            total_price=data["total_price"],
        )
