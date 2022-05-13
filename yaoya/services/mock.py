from collections.abc import Generator

import dataset


class MockDB:
    def __init__(self) -> None:
        self._dbname = "mock.db"
        self._init_mock_db()

    def connect(self) -> Generator[dataset.Database, None, None]:
        db = dataset.connect(self._dbname)
        db.begin()
        try:
            yield db
            db.commit()
        except Exception as e:
            db.rollback()
            raise e

    def _init_mock_db(self) -> None:
        self._create_mock_user_table()
        self._create_mock_item_table()
        self._create_mock_order_table()
        self._create_mock_cart_table()

    def _create_mock_user_table(self) -> None:
        pass

    def _create_mock_item_table(self) -> None:
        pass

    def _create_mock_order_table(self) -> None:
        pass

    def _create_mock_cart_table(self) -> None:
        pass
