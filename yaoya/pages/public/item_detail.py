import streamlit as st
from yaoya.models.cart import Cart
from yaoya.models.item import Item
from yaoya.models.user import User
from yaoya.pages.base import BasePage


class ItemDetailPage(BasePage):
    def render(self) -> None:
        # 商品詳細
        item: Item = self.ssm.get_item()
        if not self.render_item_detail(item):
            return

        # カートイン
        user: User = self.ssm.get_user()
        cart: Cart = self.ssm.get_cart()
        if not self.render_cart_in(user, cart, item):
            return

    def render_item_detail(self, item: Item) -> bool:
        if item is None:
            st.error("商品が選択されていません")
            return False

        show_item = {
            "商品名": item.name,
            "価格": item.price,
            "生産地": item.producing_area,
        }

        # タイトルの表示
        st.title(self.title)

        # 商品テーブルの表示
        col_size = [1, 2]
        for key, value in show_item.items():
            key_col, value_col = st.columns(col_size)
            key_col.write(key)
            value_col.write(value)

        return True

    def render_cart_in(self, user: User, cart: Cart, item: Item) -> bool:
        if user is None:
            st.warning("カートに追加するためにはログインが必要です。")
            return False

        with st.form("item_deteil_form"):
            quantity = st.number_input("数量", step=1, min_value=1, max_value=9, key="_quantity")
            kwargs = dict(cart=cart, item=item, quantity=quantity)
            st.form_submit_button(label="注文", on_click=self.cart_in, kwargs=kwargs)

        return True

    def cart_in(self, cart: Cart, item: Item, quantity: int) -> None:
        cart.add_item(item=item, quantity=int(quantity))
        st.sidebar.success("カートに追加しました")
        st.session_state["_quantity"] = 1
