import streamlit as st

from yaoya.models.cart import Cart
from yaoya.models.item import Item
from yaoya.models.user import User
from yaoya.services.const import PageId, SessionKey
from yaoya.services.item import IItemAPIClientService
from yaoya.services.order import IOrderAPIClientService
from yaoya.services.user import IUserAPIClientService


class StreamlitSessionManager:
    def __init__(
        self,
        user_api_client: IUserAPIClientService,
        item_api_client: IItemAPIClientService,
        order_api_client: IOrderAPIClientService,
    ) -> None:
        self._session_state = st.session_state
        self._session_state[SessionKey.USER_API_CLIENT.name] = user_api_client
        self._session_state[SessionKey.ITEM_API_CLIENT.name] = item_api_client
        self._session_state[SessionKey.ORDER_API_CLIENT.name] = order_api_client
        self._session_state[SessionKey.USER.name] = None
        self._session_state[SessionKey.ITEM.name] = None
        self._session_state[SessionKey.CART.name] = None
        self._session_state[SessionKey.PAGE_ID.name] = PageId.PUBLIC_LOGIN.name
        self._session_state[SessionKey.USERBOX.name] = None

    def get_user(self) -> User:
        return self._session_state[SessionKey.USER.name]

    def get_item(self) -> Item:
        return self._session_state[SessionKey.ITEM.name]

    def get_cart(self) -> Cart:
        return self._session_state[SessionKey.CART.name]

    def get_user_api_client(self) -> IUserAPIClientService:
        return self._session_state[SessionKey.USER_API_CLIENT.name]

    def get_item_api_client(self) -> IItemAPIClientService:
        return self._session_state[SessionKey.ITEM_API_CLIENT.name]

    def get_order_api_client(self) -> IOrderAPIClientService:
        return self._session_state[SessionKey.ORDER_API_CLIENT.name]

    def set_user(self, user: User) -> None:
        self._session_state[SessionKey.USER.name] = user

        # 表示するユーザ名を更新
        userbox = self._session_state[SessionKey.USERBOX.name]
        userbox.text(f"ユーザ名: {user.name}")

        # カートを更新
        self._session_state[SessionKey.CART.name] = Cart(user.user_id)

    def set_item(self, item: Item) -> None:
        self._session_state[SessionKey.ITEM.name] = item

    def set_page_id(self, page_id: PageId) -> None:
        self._session_state[SessionKey.PAGE_ID.name] = page_id.name

    def show_userbox(self) -> None:
        # コンストラクタで初期化するとStreamlitの初期化処理中にStreamlitの更新処理が入り、以下のエラーが発生する
        # StreamlitAPIException: set_page_config() can only be called once per app,
        # and must be called as the first Streamlit command in your script.
        userbox = self._session_state[SessionKey.USERBOX.name]
        user = self.get_user()
        if userbox is None or user is None:
            self._session_state[SessionKey.USERBOX.name] = st.sidebar.text("ログインしていません")
            return

        self._session_state[SessionKey.USERBOX.name] = st.sidebar.text(f"ユーザ名: {user.name}")
