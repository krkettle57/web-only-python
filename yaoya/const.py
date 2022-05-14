from enum import Enum, auto


class SessionKey(Enum):
    AUTH_API_CLIENT = auto()
    USER_API_CLIENT = auto()
    ITEM_API_CLIENT = auto()
    ORDER_API_CLIENT = auto()
    CART_API_CLIENT = auto()
    USER = auto()
    ITEM = auto()
    ORDER = auto()
    PAGE_ID = auto()
    SESSION_ID = auto()
    USERBOX = auto()


class PageId(Enum):
    PUBLIC_LOGIN = auto()
    PUBLIC_ITEM_LIST = auto()
    PUBLIC_ITEM_DETAIL = auto()
    MEMBER_CART = auto()
    MEMBER_ORDER_LIST = auto()
    MEMBER_ORDER_DETAIL = auto()


class UserRole(Enum):
    ADMIN = auto()
    MEMBER = auto()
