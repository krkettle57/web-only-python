import streamlit as st
from yaoya.pages.base import BasePage
from yaoya.services.user import IUserAPIClientService


class LoginPage(BasePage):
    def render(self) -> None:
        user_api_client: IUserAPIClientService = self.ssm.get_user_api_client()

        # ページ描画
        st.title(self.title)
        with st.form("form"):
            user_id = st.text_input("UserID")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button(label="ログイン")

        if submit_button:
            user = user_api_client.login(user_id, password)

            # ログインに失敗した場合、エラーメッセージを表示する
            if user is None:
                st.sidebar.error("ユーザID または パスワードが間違っています。")
                return

            # ログインに成功した場合、成功メッセージを表示する
            st.sidebar.success("ログインに成功しました。")
            self.ssm.set_user(user)
