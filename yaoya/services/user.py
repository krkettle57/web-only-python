from datetime import date
from typing import List, Optional, Protocol

from yaoya.models.user import User
from yaoya.services.const import UserRole


class IUserAPIClientService(Protocol):
    def login(self, user_id: str, password: str) -> Optional[User]:
        pass


class MockUserAPIClientService(IUserAPIClientService):
    def __init__(self) -> None:
        self.users: List[User] = [
            User(
                user_id="member", name="会員", birthday=date(2000, 1, 1), email="guest@example.com", role=UserRole.MEMBER
            ),
            User(
                user_id="owner", name="オーナー", birthday=date(2000, 1, 1), email="owner@example.com", role=UserRole.OWNER
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
