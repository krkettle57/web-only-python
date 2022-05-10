from random import randint
from typing import List, Optional, Protocol

from mimesis import Field, Schema
from mimesis.locales import Locale
from yaoya.models.item import Item, ItemType
from yaoya.services.base import NotFoundError


class IItemAPIClientService(Protocol):
    def get_all(self, offset: Optional[int] = None, limit: Optional[int] = None) -> List[Item]:
        pass

    def get_by_id(self, item_id: str) -> Item:
        pass

    def add_item(self, item: Item) -> None:
        pass

    def update_item(self, item_id: str, item: Item) -> None:
        pass

    def delete_item(self, item_id: str) -> None:
        pass


class MockItemAPIClientService(IItemAPIClientService):
    def __init__(self, n: int = 10, item_type: ItemType = "vegetable") -> None:
        _ = Field(locale=Locale.JA)
        schema = Schema(
            schema=lambda: {
                "item_id": _("uuid"),
                "name": _(item_type),
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
                item_type=item_type,
            )
            for data in schema.create(n)
        ]
        self.items = items

    def get_all(self, offset: Optional[int] = None, limit: Optional[int] = None) -> List[Item]:
        offset_ = 0
        limit_ = len(self.items)

        if offset is not None:
            offset_ = offset

        if limit is not None:
            limit_ = limit

        return self.items[offset_ : offset_ + limit_]

    def get_by_id(self, item_id: str) -> Item:
        for item in self.items:
            if item.item_id == item_id:
                return item

        raise NotFoundError(item_id)

    def add_item(self, item: Item) -> None:
        self.items.append(item)

    def update_item(self, item_id: str, item: Item) -> None:
        self.delete_item(item_id)
        self.add_item(item)

    def delete_item(self, item_id: str) -> None:
        for idx, item in enumerate(self.items):
            if item.item_id == item_id:
                self.items.pop(idx)
