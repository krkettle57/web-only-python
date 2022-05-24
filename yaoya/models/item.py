from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    item_id: str
    name: str
    price: int
    producing_area: str

    def to_dict(self) -> dict[str, str]:
        return dict(
            item_id=self.item_id,
            name=self.name,
            price=str(self.price),
            producing_area=self.producing_area,
        )

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Item:
        return Item(
            item_id=data["item_id"],
            name=data["name"],
            price=int(data["price"]),
            producing_area=data["producing_area"],
        )
