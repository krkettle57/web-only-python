from dataclasses import dataclass
from datetime import date
from typing import Literal

UserRole = Literal["admin", "member", "owner"]


@dataclass
class User:
    user_id: str
    name: str
    birthday: date
    email: str
    role: UserRole
