import streamlit as st
from yaoya.pages.base import BasePage
from yaoya.services.auth import AuthenticationError, IAuthAPIClientService
from yaoya.services.user import IUserAPIClientService


class LoginPage(BasePage):
    def render(self) -> None:
        auth_api_client: IAuthAPIClientService = self.ssm.get_auth_api_client()
        user_api_client: IUserAPIClientService = self.ssm.get_user_api_client()

        # ページ描画
        st.title(self.title)
        with st.form("form"):
            user_id = st.text_input("UserID")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button(label="ログイン")

        if submit_button:
            try:
                session_id = auth_api_client.login(user_id, password)
                user = user_api_client.get_by_session_id(session_id)
            except AuthenticationError:
                st.sidebar.error("ユーザID または パスワードが間違っています。")
                return

            # ログインに成功した場合、成功メッセージを表示する
            st.sidebar.success("ログインに成功しました。")
            self.ssm.set_user(user)
