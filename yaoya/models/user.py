from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from yaoya.const import UserRole
from yaoya.models.base import BaseDataModel


@dataclass(frozen=True)
class User(BaseDataModel):
    user_id: str
    name: str
    birthday: date
    email: str
    role: UserRole

    def to_dict(self) -> dict:
        return dict(
            user_id=self.user_id,
            name=self.name,
            birthday=self.birthday,
            email=self.email,
            role=self.role.name,
        )

    @classmethod
    def from_dict(cls, data: dict) -> User:
        return User(
            user_id=data["user_id"],
            name=data["name"],
            birthday=data["birthday"],
            email=data["email"],
            role=UserRole[data["role"]],
        )
