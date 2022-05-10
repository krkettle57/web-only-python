from enum import Enum, auto


class SessionKey(Enum):
    USER_API_CLIENT = auto()
    ITEM_API_CLIENT = auto()
    ORDER_API_CLIENT = auto()
    USER = auto()
    ITEM = auto()
    CART = auto()
    PAGE_ID = auto()
    USERBOX = auto()


class PageId(Enum):
    PUBLIC_LOGIN = auto()
    PUBLIC_ITEM_LIST = auto()
    PUBLIC_ITEM_DETAIL = auto()
