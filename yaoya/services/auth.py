from typing import Protocol

from yaoya.models.cart import Cart
from yaoya.models.session import Session
from yaoya.services.mock import MockSessionDB


class IAuthAPIClientService(Protocol):
    def login(self, user_id: str, password: str) -> str:
        pass


class MockAuthAPIClientService(IAuthAPIClientService):
    def __init__(self, session_db: MockSessionDB) -> None:
        self.session_db = session_db

    def login(self, user_id: str, password: str) -> str:
        # 本来であれば認証処理が入るが、Mockのため実装しない
        session = Session(user_id=user_id, cart=Cart(user_id))
        with self.session_db.connect() as db:
            db.insert(session.to_dict())

        return session.session_id
