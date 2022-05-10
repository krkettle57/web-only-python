import streamlit as st

from yaoya.init_app import init_app, init_pages, init_session

if not st.session_state.get("is_started", False):
    ssm = init_session()
    pages = init_pages(ssm)
    app = init_app(ssm, pages)
    st.session_state["is_started"] = True
    st.session_state["app"] = app
    st.set_page_config(page_title="八百屋さんEC", layout="wide")

app = st.session_state.get("app", None)
if app is not None:
    app.render()
