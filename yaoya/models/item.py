from dataclasses import dataclass


@dataclass
class Item:
    item_id: str
    name: str
    price: int
    producing_area: str
