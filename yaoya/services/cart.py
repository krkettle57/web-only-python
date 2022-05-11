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

    def get_by_user_id(self, user_id: str) -> Cart:
        return self.carts[user_id]

    def add_item(self, user_id: str, item: Item, quantity: int) -> None:
        if user_id not in self.carts:
            self.carts[user_id] = Cart(user_id=user_id)

        cart_item = CartItem(
            item_no=len(self.carts[user_id].cart_items) + 1,
            item=item,
            quantity=quantity,
        )
        self.carts[user_id].cart_items.append(cart_item)

    def clear_cart(self, user_id: str) -> None:
        self.carts[user_id].cart_items = []
