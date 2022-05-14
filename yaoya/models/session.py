from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from yaoya.models.base import BaseDataModel
from yaoya.models.cart import Cart


@dataclass(frozen=True)
class Session(BaseDataModel):
    user_id: str
    cart: Cart
    session_id: str = str(uuid4())

    def to_dict(self) -> dict:
        return dict(
            session_id=self.session_id,
            user_id=self.user_id,
            cart=self.cart.to_dict(),
        )

    @classmethod
    def from_dict(cls, data: dict) -> Session:
        return Session(
            session_id=data["session_id"],
            user_id=data["user_id"],
            cart=Cart.from_dict(data["cart"]),
        )
