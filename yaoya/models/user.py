from dataclasses import dataclass
from datetime import date

from yaoya.services.const import UserRole


@dataclass
class User:
    user_id: str
    name: str
    birthday: date
    email: str
    role: UserRole
