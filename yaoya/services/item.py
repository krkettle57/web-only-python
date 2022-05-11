from random import randint
from typing import Optional, Protocol

from mimesis import Field, Schema
from mimesis.locales import Locale
from yaoya.models.item import Item


class IItemAPIClientService(Protocol):
    def get_all(self, offset: Optional[int] = None, limit: Optional[int] = None) -> list[Item]:
        pass

    def get_by_id(self, item_id: str) -> Item:
        pass


class MockItemAPIClientService(IItemAPIClientService):
    def __init__(self, n: int = 10) -> None:
        _ = Field(locale=Locale.JA)
        schema = Schema(
            schema=lambda: {
                "item_id": _("uuid"),
                "name": _("vegetable"),
                "price": randint(1, 5) * 100 - 2,
                "producing_area": _("prefecture"),
            }
        )
        items = [
            Item(
                item_id=data["item_id"],
                name=data["name"],
                price=data["price"],
                producing_area=data["producing_area"],
            )
            for data in schema.create(n)
        ]
        self.items = items

    def get_all(self, offset: Optional[int] = None, limit: Optional[int] = None) -> list[Item]:
        offset_ = 0
        limit_ = len(self.items)

        if offset is not None:
            offset_ = offset

        if limit is not None:
            limit_ = limit

        return self.items[offset_ : offset_ + limit_]
