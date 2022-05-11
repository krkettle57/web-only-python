from yaoya.app import MultiPageApp
from yaoya.const import PageId
from yaoya.pages.base import BasePage
from yaoya.pages.member.cart import CartPage
from yaoya.pages.member.order_detail import OrderDetailPage
from yaoya.pages.member.order_list import OrderListPage
from yaoya.pages.public.item_detail import ItemDetailPage
from yaoya.pages.public.item_list import ItemListPage
from yaoya.pages.public.login import LoginPage
from yaoya.services.item import MockItemAPIClientService
from yaoya.services.order import MockOrderAPIClientService
from yaoya.services.user import MockUserAPIClientService
from yaoya.sesseion import StreamlitSessionManager


def init_session() -> StreamlitSessionManager:
    ssm = StreamlitSessionManager(
        user_api_client=MockUserAPIClientService(),
        item_api_client=MockItemAPIClientService(),
        order_api_client=MockOrderAPIClientService(),
    )
    return ssm


def init_pages(ssm: StreamlitSessionManager) -> list[BasePage]:
    pages = [
        LoginPage(page_id=PageId.PUBLIC_LOGIN.name, title="ログイン", ssm=ssm),
        ItemListPage(page_id=PageId.PUBLIC_ITEM_LIST.name, title="商品一覧", ssm=ssm),
        ItemDetailPage(page_id=PageId.PUBLIC_ITEM_DETAIL.name, title="商品詳細", ssm=ssm),
        CartPage(page_id=PageId.MEMBER_CART.name, title="カート", ssm=ssm),
        OrderListPage(page_id=PageId.MEMBER_ORDER_LIST.name, title="注文一覧", ssm=ssm),
        OrderDetailPage(page_id=PageId.MEMBER_ORDER_DETAIL.name, title="注文詳細", ssm=ssm),
    ]
    return pages


def init_app(ssm: StreamlitSessionManager, pages: list[BasePage]) -> MultiPageApp:
    app = MultiPageApp(ssm, pages)
    return app
