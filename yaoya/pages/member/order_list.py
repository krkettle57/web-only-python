import streamlit as st
from yaoya.const import PageId
from yaoya.models.order import Order
from yaoya.pages.member.base import MemberPage
from yaoya.services.base import NotFoundError


class OrderListPage(MemberPage):
    def render(self) -> None:
        if not self.validate_user():
            return

        session_id = self.ssm.get_session_id()
        order_api_client = self.ssm.get_order_api_client()

        # タイトル表示
        st.title(self.title)

        # カートテーブル表示
        col_size = [1, 2, 2, 4, 2]
        columns = st.columns(col_size)
        headers = ["No", "注文ID", "合計金額", "注文日付", ""]
        for col, field_name in zip(columns, headers):
            col.write(field_name)

        # 注文一覧を取得
        try:
            orders = order_api_client.get_orders(session_id)
        except NotFoundError:
            st.warning("注文履歴はありません。")
            return

        for index, order in enumerate(orders):
            (
                col_no,
                col_id,
                col_total,
                col_date,
                col_button,
            ) = st.columns(col_size)
            col_no.write(index + 1)
            col_id.write(order.order_id[-8:])
            col_total.write(order.total_price)
            col_date.write(order.ordered_at.strftime("%Y-%m-%d %H:%M:%S"))
            col_button.button("詳細", on_click=self.order_detail, args=(order,))

    def order_detail(self, order: Order) -> None:
        self.ssm.set_order(order)
        self.ssm.set_page_id(PageId.MEMBER_ORDER_DETAIL)
