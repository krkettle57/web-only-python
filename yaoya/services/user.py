from typing import Optional, Protocol

import dataset
from yaoya.models.user import User
from yaoya.services.mock import MockDB


class IUserAPIClientService(Protocol):
    def login(self, user_id: str, password: str) -> Optional[User]:
        pass


class MockUserAPIClientService(IUserAPIClientService):
    def __init__(self, mockdb: MockDB) -> None:
        self.mockdb = mockdb

    def login(self, user_id: str, password: str) -> Optional[User]:
        with self.mockdb.connect() as db:
            table: dataset.Table = db["users"]
            user_data = table.find_one(user_id=user_id)

        if user_data is None:
            return None

        return User.from_dict(user_data)
