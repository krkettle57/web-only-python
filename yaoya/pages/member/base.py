import streamlit as st
from yaoya.const import UserRole
from yaoya.pages.base import BasePage


class MemberPage(BasePage):
    def validate_user(self) -> bool:
        user = self.ssm.get_user()
        if (user is None) or (user.role not in (UserRole.MEMBER, UserRole.ADMIN)):
            st.warning("会員専用ページです")
            return False

        return True
