from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Item:
    item_id: str
    name: str
    price: int
    producing_area: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> Item:
        return Item(
            item_id=data["item_id"],
            name=data["name"],
            price=data["price"],
            producing_area=data["producing_area"],
        )
