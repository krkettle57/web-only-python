import sqlite3
from pathlib import Path
from random import randint
from typing import Protocol

from mimesis import Field, Schema
from mimesis.locales import Locale
from yaoya.models.item import Item


class IItemAPIClientService(Protocol):
    def get_all(self) -> list[Item]:
        pass


class MockItemAPIClientService(IItemAPIClientService):
    def __init__(self, n: int = 10) -> None:
        self.dbname = "mock_items.db"
        if not Path(self.dbname).exists():
            mock_items = self.create_mock_items(n)
            self.init_item_table(mock_items)

    def create_mock_items(self, n: int) -> list[Item]:
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
        return mock_items

    def init_item_table(self, mock_items: list[Item]) -> None:
        conn = sqlite3.connect(self.dbname)
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE items(
                item_id TEXT PRIMARY KEY,
                name TEXT,
                price INTEGER,
                producing_area TEXT
            )
            """
        )
        for item in mock_items:
            cur.execute(
                """
            INSERT INTO items
            VALUES (
                :item_id,
                :name,
                :price,
                :producing_area
            )
            """,
                (
                    item.item_id,
                    item.name,
                    item.price,
                    item.producing_area,
                ),
            )
        conn.commit()
        conn.close()

    def get_all(self) -> list[Item]:
        conn = sqlite3.connect(self.dbname)
        cur = conn.cursor()
        cur.execute("SELECT item_id, name, price, producing_area FROM items")
        items_data = cur.fetchall()
        return [
            Item(
                item_id=item_data[0],
                name=item_data[1],
                price=item_data[2],
                producing_area=item_data[3],
            )
            for item_data in items_data
        ]
