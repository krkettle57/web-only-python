import streamlit as st
from yaoya.models.cart import Cart
from yaoya.models.order import Order
from yaoya.pages.member.base import MemberPage


class CartPage(MemberPage):
    def render(self) -> None:
        if not self.validate_user():
            return

        cart = self.ssm.get_cart()

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

        st.button("注文", on_click=self.order_commit, args=(cart,), disabled=len(cart.cart_items) == 0)

    def order_commit(self, cart: Cart) -> None:
        order_api_client = self.ssm.get_order_api_client()
        order = Order(user_id=cart.user_id)
        for cart_item in cart.cart_items:
            order.add_detail(
                item_id=cart_item.item.item_id,
                unit_price=cart_item.item.price,
                quantity=cart_item.quantity,
            )
        order_api_client.insert(order)
        cart.clear()
        st.sidebar.success("注文が完了しました")
