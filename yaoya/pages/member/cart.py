import streamlit as st
from yaoya.models.cart import Cart
from yaoya.pages.member.base import MemberPage
from yaoya.services.cart import ICartAPIClientService


class CartPage(MemberPage):
    def render(self) -> None:
        if not self.validate_user():
            return

        user = self.ssm.get_user()
        cart_api_client = self.ssm.get_cart_api_client()
        cart = cart_api_client.get_by_user_id(user.user_id)

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

        for cart_item in cart.cart_items:
            (
                no_col,
                name_col,
                price_col,
                q_col,
            ) = st.columns(col_size)
            no_col.write(cart_item.item_no)
            name_col.write(cart_item.item.name)
            price_col.write(cart_item.item.price)
            q_col.write(cart_item.quantity)

        st.button("注文", on_click=self.order_commit, args=(cart, cart_api_client))

    def order_commit(self, cart: Cart, cart_api_client: ICartAPIClientService) -> None:
        order_api_client = self.ssm.get_order_api_client()
        order_api_client.order_commit(cart)
        cart_api_client.clear_cart(cart.user_id)
        st.sidebar.success("注文が完了しました")
