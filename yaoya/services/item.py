from typing import Protocol

import dataset
from yaoya.models.item import Item
from yaoya.services.mock import MockDB


class IItemAPIClientService(Protocol):
    def get_all(self) -> list[Item]:
        pass


class MockItemAPIClientService(IItemAPIClientService):
    def __init__(self, mockdb: MockDB) -> None:
        self.mockdb = mockdb

    def get_all(self) -> list[Item]:
        with self.mockdb.connect() as db:
            table: dataset.Table = db["items"]
            items_data = table.all()

        return [Item.from_dict(item_data) for item_data in items_data]
