import streamlit as st
from yaoya.models.order import Order
from yaoya.pages.member.base import MemberPage


class OrderDetailPage(MemberPage):
    def render(self) -> None:
        if not self.validate_user():
            return

        order = self.ssm.get_order()

        # タイトル表示
        st.title(self.title)

        # 注文情報表示
        if not self._render_order(order):
            return

        # 注文詳細一覧表示
        if not self._render_order_detail(order):
            return

    def _render_order(self, order: Order) -> bool:
        if order is None:
            st.error("商品が選択されていません")
            return False

        show_order = {
            "注文ID": order.order_id,
            "合計金額": order.total_price,
            "注文日付": order.ordered_at.strftime("%Y-%m-%d %H:%M:%S"),
        }

        # サブタイトルの表示
        st.subheader("注文情報")

        # 注文テーブルの表示
        col_size = [1, 2]
        for key, value in show_order.items():
            key_col, value_col = st.columns(col_size)
            key_col.write(key)
            value_col.write(value)

        return True

    def _render_order_detail(self, order: Order) -> bool:
        # サブタイトル表示
        st.subheader("注文詳細一覧")

        # 注文詳細テーブル表示
        col_size = [1, 2, 2, 2]
        columns = st.columns(col_size)
        headers = ["No", "商品名", "単価", "数量"]
        for col, field_name in zip(columns, headers):
            col.write(field_name)

        for order_detail in order.details:
            (
                no_col,
                name_col,
                price_col,
                q_col,
            ) = st.columns(col_size)
            no_col.write(order_detail.order_no)
            name_col.write(order_detail.item.name)
            price_col.write(order_detail.item.price)
            q_col.write(order_detail.quantity)

        return True
