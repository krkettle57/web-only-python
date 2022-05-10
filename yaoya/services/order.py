from typing import List, Protocol

from yaoya.models.order import Order
from yaoya.services.base import NotFoundError


class IOrderAPIClientService(Protocol):
    def get_all(self) -> List[Order]:
        pass

    def get_by_id(self, order_id: str) -> Order:
        pass

    def insert(self, order: Order) -> None:
        pass


class MockOrderAPIClientService(IOrderAPIClientService):
    def __init__(self) -> None:
        self.orders: List[Order] = []

    def get_all(self) -> List[Order]:
        return self.orders

    def get_by_id(self, order_id: str) -> Order:
        for order in self.orders:
            if order.order_id == order_id:
                return order

        raise NotFoundError(order_id)

    def insert(self, order: Order) -> None:
        self.orders.append(order)
