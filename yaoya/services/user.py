from datetime import date
from typing import Optional, Protocol

from yaoya.const import UserRole
from yaoya.models.user import User


class IUserAPIClientService(Protocol):
    def login(self, user_id: str, password: str) -> Optional[User]:
        pass


class MockUserAPIClientService(IUserAPIClientService):
    def __init__(self) -> None:
        self.users: list[User] = [
            User(
                user_id="member", name="会員", birthday=date(2000, 1, 1), email="guest@example.com", role=UserRole.MEMBER
            ),
            User(
                user_id="admin", name="管理者", birthday=date(2000, 1, 1), email="admin@example.com", role=UserRole.ADMIN
            ),
        ]

    def login(self, user_id: str, password: str) -> Optional[User]:
        for user in self.users:
            if user.user_id == user_id:
                return user

        return None
