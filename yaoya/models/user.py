from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from yaoya.const import UserRole


@dataclass(frozen=True)
class User:
    user_id: str
    name: str
    birthday: date
    email: str
    role: UserRole

    @classmethod
    def from_dict(cls, data: dict) -> User:
        return User(
            user_id=data["user_id"],
            name=data["name"],
            birthday=data["birthday"],
            email=data["email"],
            role=data["role"],
        )
