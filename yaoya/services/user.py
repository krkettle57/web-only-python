from typing import Protocol

import dataset
from tinydb import Query
from yaoya.models.user import User
from yaoya.services.mock import MockDB, MockSessionDB

from services.base import NotFoundError


class IUserAPIClientService(Protocol):
    def get_by_user_id(self, user_id: str) -> User:
        pass

    def get_by_session_id(self, session_id: str) -> User:
        pass


class MockUserAPIClientService(IUserAPIClientService):
    def __init__(self, mockdb: MockDB, session_db: MockSessionDB) -> None:
        self.mockdb = mockdb
        self.session_db = session_db

    def get_by_user_id(self, user_id: str) -> User:
        with self.mockdb.connect() as db:
            table: dataset.Table = db["users"]
            user_data = table.find_one(user_id=user_id)

        if user_data is None:
            raise NotFoundError()

        return User.from_dict(user_data)

    def get_by_session_id(self, session_id: str) -> User:
        user_id = self._get_user_id(session_id)
        user = self.get_by_user_id(user_id)
        return user

    def _get_user_id(self, session_id: str) -> str:
        with self.session_db.connect() as db:
            query = Query()
            doc = db.search(query.session_id == session_id)

        return doc[0]["user_id"]
