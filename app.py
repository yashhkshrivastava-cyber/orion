import streamlit as st

from pages.dashboard import render_dashboard
from pages.data_management import render_data_management
from pages.home import render_home

st.set_page_config(page_title="Orion", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "home"

PAGES = {
    "home": render_home,
    "dashboard": render_dashboard,
    "data": render_data_management,
}

PAGES[st.session_state.page]()
