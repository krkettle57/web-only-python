import sqlite3
from datetime import date, datetime
from pathlib import Path
from typing import Optional, Protocol

from yaoya.const import UserRole
from yaoya.models.user import User


class IUserAPIClientService(Protocol):
    def login(self, user_id: str, password: str) -> Optional[User]:
        pass


class MockUserAPIClientService(IUserAPIClientService):
    def __init__(self) -> None:
        self.dbname = "mock_users.db"
        if not Path(self.dbname).exists():
            mock_users = [
                User(
                    user_id="member",
                    name="会員",
                    birthday=date(2000, 1, 1),
                    email="guest@example.com",
                    role=UserRole.MEMBER,
                ),
                User(
                    user_id="admin",
                    name="管理者",
                    birthday=date(2000, 1, 1),
                    email="admin@example.com",
                    role=UserRole.ADMIN,
                ),
            ]
            self.init_user_table(mock_users)

    def init_user_table(self, mock_users: list[User]) -> None:
        conn = sqlite3.connect(self.dbname)
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE users(
                user_id TEXT PRIMARY KEY,
                name TEXT,
                birthday TEXT,
                email TEXT,
                role TEXT
            )
            """
        )
        for user in mock_users:
            cur.execute(
                """
            INSERT INTO users
            VALUES (
                :user_id,
                :name,
                :birthday,
                :email,
                :role
            )
            """,
                (
                    user.user_id,
                    user.name,
                    user.birthday.isoformat(),
                    user.email,
                    user.role.name,
                ),
            )
        conn.commit()
        conn.close()

    def login(self, user_id: str, password: str) -> Optional[User]:
        conn = sqlite3.connect(self.dbname)
        cur = conn.cursor()
        cur.execute("SELECT user_id, name, birthday, email, role FROM users WHERE user_id = ?", (user_id,))
        user_data = cur.fetchone()
        if user_data is None:
            return None

        return User(
            user_id=user_data[0],
            name=user_data[1],
            birthday=datetime.fromisoformat(user_data[2]),
            email=user_data[3],
            role=UserRole[user_data[4]],
        )
