from typing import Protocol

from yaoya.models.cart import Cart, CartItem
from yaoya.models.item import Item


class ICartAPIClientService(Protocol):
    def get_by_user_id(self, user_id: str) -> Cart:
        pass

    def add_item(self, user_id: str, item: Item, quantity: int) -> None:
        pass

    def clear_cart(self, user_id: str) -> None:
        pass


class MockCartAPIClientService(ICartAPIClientService):
    def __init__(self) -> None:
        self.carts: dict[str, Cart] = dict()

    def _init_cart(self, user_id: str) -> None:
        if user_id not in self.carts:
            self.carts[user_id] = Cart(user_id=user_id, cart_items=list(), total_price=0)

    def get_by_user_id(self, user_id: str) -> Cart:
        self._init_cart(user_id)
        return self.carts[user_id]

    def add_item(self, user_id: str, item: Item, quantity: int) -> None:
        self._init_cart(user_id)

        # カートアイテム生成
        cart_item = CartItem(
            item_no=len(self.carts[user_id].cart_items) + 1,
            item=item,
            quantity=quantity,
        )

        # カート更新
        cart = self.carts[user_id]
        self.carts[user_id] = Cart(
            user_id=cart.user_id,
            cart_items=[*cart.cart_items, cart_item],
            total_price=cart.total_price + (item.price * quantity),
        )

    def clear_cart(self, user_id: str) -> None:
        self.carts[user_id] = Cart(user_id=user_id, cart_items=list(), total_price=0)
