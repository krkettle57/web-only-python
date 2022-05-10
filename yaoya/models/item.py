from dataclasses import dataclass
from typing import Literal

ItemType = Literal["vegetable", "fruit"]


@dataclass
class Item:
    item_id: str
    name: str
    price: int
    producing_area: str
    item_type: ItemType
