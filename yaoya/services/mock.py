from collections.abc import Generator
from contextlib import contextmanager
from datetime import date
from pathlib import Path
from random import randint

import dataset
from mimesis import Field, Schema
from mimesis.locales import Locale
from tinydb import TinyDB
from yaoya.const import UserRole
from yaoya.models.item import Item
from yaoya.models.user import User


class MockDB:
    def __init__(self) -> None:
        self._dbname = "sqlite:///mock.db"
        self._init_mock_db()

    @contextmanager
    def connect(self) -> Generator[dataset.Database, None, None]:
        db = dataset.connect(self._dbname)
        db.begin()
        try:
            yield db
            db.commit()
        except Exception as e:
            db.rollback()
            raise e

    def _init_mock_db(self) -> None:
        self._create_mock_user_table()
        self._create_mock_item_table()
        self._create_mock_order_table()
        self._create_mock_cart_table()

    def _create_mock_user_table(self) -> None:
        mock_users = [
            User(
                user_id="member",
                name="会員",
                birthday=date(2000, 1, 1),
                email="guest@example.com",
                role=UserRole.MEMBER,
            ),
            User(
                user_id="admin",
                name="管理者",
                birthday=date(2000, 1, 1),
                email="admin@example.com",
                role=UserRole.ADMIN,
            ),
        ]
        with self.connect() as db:
            table: dataset.Table = db["users"]
            for mock_user in mock_users:
                table.insert(mock_user.to_dict())

    def _create_mock_item_table(self, n: int = 10) -> None:
        _ = Field(locale=Locale.JA)
        schema = Schema(
            schema=lambda: {
                "item_id": _("uuid"),
                "name": _("vegetable"),
                "price": randint(1, 5) * 100 - 2,
                "producing_area": _("prefecture"),
            }
        )
        mock_items = [
            Item(
                item_id=data["item_id"],
                name=data["name"],
                price=data["price"],
                producing_area=data["producing_area"],
            )
            for data in schema.create(n)
        ]
        with self.connect() as db:
            table: dataset.Table = db["items"]
            for mock_item in mock_items:
                table.insert(mock_item.to_dict())

    def _create_mock_order_table(self) -> None:
        pass

    def _create_mock_cart_table(self) -> None:
        pass


class MockSessionDB:
    def __init__(self, dbpath: Path) -> None:
        self._db = TinyDB(dbpath)

    @contextmanager
    def connect(self) -> Generator[TinyDB, None, None]:
        try:
            yield self._db
        except Exception as e:
            raise e
