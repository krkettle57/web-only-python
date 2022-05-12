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
