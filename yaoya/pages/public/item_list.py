import streamlit as st
from yaoya.models.item import Item
from yaoya.pages.base import BasePage
from yaoya.services.const import PageId
from yaoya.services.item import IItemAPIClientService


class ItemListPage(BasePage):
    def render(self) -> None:
        item_api_client: IItemAPIClientService = self.ssm.get_item_api_client()

        # タイトルの表示
        st.title(self.title)

        # 商品テーブルの表示
        col_size = [1, 2, 2, 2]
        columns = st.columns(col_size)
        headers = ["No", "名前", "価格", ""]
        for col, field_name in zip(columns, headers):
            col.write(field_name)

        for index, item in enumerate(item_api_client.get_all()):
            (
                no_col,
                name_col,
                price_col,
                button_col,
            ) = st.columns(col_size)
            no_col.write(index + 1)
            name_col.write(item.name)
            price_col.write(item.price)
            button_col.button("詳細", key=item.item_id, on_click=self.detail_on_clink, args=(item,))

    def detail_on_clink(self, item: Item) -> None:
        self.ssm.set_item(item)
        self.ssm.set_page_id(PageId.PUBLIC_ITEM_DETAIL)
