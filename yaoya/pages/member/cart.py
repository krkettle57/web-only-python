import streamlit as st
from yaoya.pages.member.base import MemberPage


class CartPage(MemberPage):
    def render(self) -> None:
        if not self.validate_user():
            return

        session_id = self.ssm.get_session_id()
        cart_api_client = self.ssm.get_cart_api_client()
        cart = cart_api_client.get_cart(session_id)

        if len(cart.cart_items) == 0:
            st.warning("カートに入っている商品はありません。")
            return

        # タイトル表示
        st.title(self.title)

        # カートテーブル表示
        col_size = [1, 2, 2, 2]
        columns = st.columns(col_size)
        headers = ["No", "商品名", "単価", "数量"]
        for col, field_name in zip(columns, headers):
            col.write(field_name)

        for idx, cart_item in enumerate(cart.cart_items):
            (
                no_col,
                name_col,
                price_col,
                q_col,
            ) = st.columns(col_size)
            no_col.write(idx + 1)
            name_col.write(cart_item.item.name)
            price_col.write(cart_item.item.price)
            q_col.write(cart_item.quantity)

        # 合計金額表示
        st.text(f"合計金額: {cart.total_price}")

        st.button("注文", on_click=self._order_commit)

    def _order_commit(self) -> None:
        session_id = self.ssm.get_session_id()
        order_api_client = self.ssm.get_order_api_client()
        cart_api_client = self.ssm.get_cart_api_client()

        order_api_client.order_commit(session_id)
        cart_api_client.clear_cart(session_id)
        st.sidebar.success("注文が完了しました")
