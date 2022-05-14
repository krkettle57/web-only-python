import json
from datetime import datetime, timedelta, timezone
from typing import Protocol
from uuid import uuid4

import dataset
from tinydb import Query
from yaoya.models.cart import Cart
from yaoya.models.order import Order, OrderDetail
from yaoya.models.session import Session
from yaoya.services.mock import MockDB, MockSessionDB

JST = timezone(timedelta(hours=+9), "JST")


class IOrderAPIClientService(Protocol):
    def get_orders(self, session_id: str) -> list[Order]:
        pass

    def order_commit(self, session_id: str) -> None:
        pass


class MockOrderAPIClientService(IOrderAPIClientService):
    def __init__(self, mockdb: MockDB, session_db: MockSessionDB) -> None:
        self.mockdb = mockdb
        self.session_db = session_db

    def get_orders(self, session_id: str) -> list[Order]:
        session = self._get_session(session_id)

        with self.mockdb.connect() as db:
            orders_table: dataset.Table = db["orders"]
            orders_data = list(orders_table.find(user_id=session.user_id))
            orders = [Order.from_dict(json.loads(order_data["order_body"])) for order_data in orders_data]

        return orders

    def order_commit(self, session_id: str) -> None:
        session = self._get_session(session_id)

        order = self._create_order_from_cart(session.cart)
        with self.mockdb.connect() as db:
            # 注文テーブル
            orders_table: dataset.Table = db["orders"]
            order_data = dict(
                order_id=order.order_id,
                user_id=order.user_id,
                order_body=json.dumps(order.to_dict(), default=str),
            )
            orders_table.insert(order_data)

    def _create_order_from_cart(self, cart: Cart) -> Order:
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
        order = Order(
            order_id=str(uuid4()),
            user_id=cart.user_id,
            total_price=cart.total_price,
            ordered_at=datetime.now(JST),
            details=order_details,
        )
        return order

    def _get_session(self, session_id: str) -> Session:
        with self.session_db.connect() as db:
            query = Query()
            doc = db.search(query.session_id == session_id)[0]
            session = Session.from_dict(doc)

        return session
