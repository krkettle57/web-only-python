from __future__ import annotations

import json
from dataclasses import dataclass, field

from yaoya.models.base import BaseDataModel
from yaoya.models.item import Item


@dataclass(frozen=True)
class CartItem(BaseDataModel):
    item: Item
    quantity: int = 0

    def to_dict(self) -> dict[str, str]:
        item_dict = self.item.to_dict()
        return dict(
            item=json.dumps(item_dict),
            quantity=str(self.quantity),
        )

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> CartItem:
        item_data = json.loads(data["item"])
        return CartItem(
            item=Item.from_dict(item_data),
            quantity=int(data["quantity"]),
        )


@dataclass(frozen=True)
class Cart(BaseDataModel):
    user_id: str
    cart_items: list[CartItem] = field(default_factory=list)
    total_price: int = 0

    def to_dict(self) -> dict[str, str]:
        cart_items = [cart_item.to_dict() for cart_item in self.cart_items]
        return dict(
            user_id=self.user_id,
            cart_items=json.dumps(cart_items),
            total_price=str(self.total_price),
        )

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Cart:
        cart_items = [CartItem.from_dict(cart_item_dict) for cart_item_dict in json.loads(data["cart_items"])]
        return Cart(
            user_id=data["user_id"],
            cart_items=cart_items,
            total_price=int(data["total_price"]),
        )
