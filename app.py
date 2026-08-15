import streamlit as st

from views.dashboard import render_dashboard
from views.data_management import render_data_management
from views.home import render_home

st.set_page_config(page_title="Orion", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "home"

PAGES = {
    "home": ("Home", render_home),
    "dashboard": ("Dashboard", render_dashboard),
    "data": ("Data Management", render_data_management),
}

with st.sidebar:
    st.title("Orion")
    st.divider()

    for page_id, (label, _) in PAGES.items():
        if st.button(label, use_container_width=True, type="primary" if st.session_state.page == page_id else "secondary"):
            st.session_state.page = page_id
            st.rerun()

PAGES[st.session_state.page][1]()
