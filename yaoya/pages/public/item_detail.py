import streamlit as st
from yaoya.models.cart import CartItem
from yaoya.models.item import Item
from yaoya.pages.base import BasePage


class ItemDetailPage(BasePage):
    def render(self) -> None:
        # タイトルの表示
        st.title(self.title)

        # 商品詳細
        item = self.ssm.get_item()
        if item is None:
            st.error("商品が選択されていません")
            return

        self._render_item_detail(item)

        # カートイン
        user = self.ssm.get_user()
        session_id = self.ssm.get_session_id()
        if user is None or session_id is None:
            st.warning("カートに追加するためにはログインが必要です。")
            return

        self._render_cart_in(item, session_id)

    def _render_item_detail(self, item: Item) -> None:
        show_item = {
            "商品名": item.name,
            "価格": item.price,
            "生産地": item.producing_area,
        }

        # 商品詳細テーブルの表示
        col_size = [1, 2]
        for key, value in show_item.items():
            key_col, value_col = st.columns(col_size)
            key_col.write(key)
            value_col.write(value)

    def _render_cart_in(self, item: Item, session_id: str) -> None:
        with st.form("item_deteil_form"):
            st.number_input("数量", step=1, min_value=1, max_value=9, key="_quantity")
            kwargs = dict(item=item, session_id=session_id)
            st.form_submit_button(label="カートに追加", on_click=self._cart_in, kwargs=kwargs)

    def _cart_in(self, item: Item, session_id: str) -> None:
        cart_api_client = self.ssm.get_cart_api_client()
        cart_item = CartItem(
            item=item,
            quantity=st.session_state["_quantity"],
        )
        cart_api_client.add_item(
            session_id=session_id,
            cart_item=cart_item,
        )
        st.sidebar.success("カートに追加しました")
        st.session_state["_quantity"] = 1
