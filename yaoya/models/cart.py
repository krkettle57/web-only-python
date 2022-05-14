from __future__ import annotations

from dataclasses import dataclass

from yaoya.models.base import BaseDataModel
from yaoya.models.item import Item


@dataclass(frozen=True)
class CartItem(BaseDataModel):
    item: Item
    quantity: int = 0

    def to_dict(self) -> dict:
        return dict(
            item=self.item.to_dict(),
            quantity=self.quantity,
        )

    @classmethod
    def from_dict(cls, data: dict) -> CartItem:
        return CartItem(
            item=data["item"],
            quantity=data["quantity"],
        )


@dataclass(frozen=True)
class Cart(BaseDataModel):
    user_id: str
    cart_items: list[CartItem] = list()
    total_price: int = 0

    def to_dict(self) -> dict:
        return dict(
            user_id=self.user_id,
            cart_items=[cart_item.to_dict() for cart_item in self.cart_items],
            total_price=self.total_price,
        )

    @classmethod
    def from_dict(cls, data: dict) -> Cart:
        cart_items = [CartItem.from_dict(cart_item_data) for cart_item_data in data["cart_items"]]
        return Cart(
            user_id=data["user_id"],
            cart_items=cart_items,
            total_price=data["total_price"],
        )
