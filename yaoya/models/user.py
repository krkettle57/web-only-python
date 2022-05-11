from datetime import date
from typing import NamedTuple

from yaoya.const import UserRole


class User(NamedTuple):
    user_id: str
    name: str
    birthday: date
    email: str
    role: UserRole
