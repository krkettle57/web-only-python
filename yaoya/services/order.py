from typing import Protocol

from yaoya.models.cart import Cart
from yaoya.models.order import Order, OrderDetail
from yaoya.services.base import NotFoundError


class IOrderAPIClientService(Protocol):
    def get_by_user_id(self, user_id: str) -> list[Order]:
        pass

    def insert(self, order: Order) -> None:
        pass

    def order_commit(self, cart: Cart) -> None:
        pass


class MockOrderAPIClientService(IOrderAPIClientService):
    def __init__(self) -> None:
        self.orders: list[Order] = []

    def get_by_user_id(self, user_id: str) -> list[Order]:
        orders = [order for order in self.orders if order.user_id == user_id]
        if len(orders) == 0:
            raise NotFoundError(user_id)

        return orders

    def insert(self, order: Order) -> None:
        self.orders.append(order)

    # TODO: sqliteからcartを取得するように修正する(Cartの代わりにuser_idを取得)
    def order_commit(self, cart: Cart) -> None:
        total_price = 0
        order_details = []
        for idx, cart_item in enumerate(cart.cart_items):
            subtotal_price = cart_item.item.price * cart_item.quantity
            order_detail = OrderDetail(
                order_no=idx + 1,
                item=cart_item.item,
                quantity=cart_item.quantity,
                subtotal_price=subtotal_price,
            )
            order_details.append(order_detail)
            total_price += subtotal_price
        order = Order(user_id=cart.user_id, total_price=total_price, details=order_details)
        self.orders.append(order)
