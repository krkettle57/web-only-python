from typing import NamedTuple


class Item(NamedTuple):
    item_id: str
    name: str
    price: int
    producing_area: str
