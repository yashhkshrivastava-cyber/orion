import streamlit as st

from services.auth_service import (
    can_access_page,
    ensure_default_admin,
    get_current_user,
    logout,
    refresh_current_user,
)
from views.admin import render_admin
from views.dashboard import render_dashboard
from views.data_management import render_data_management
from views.home import render_home
from views.login import render_login

st.set_page_config(page_title="Orion", layout="wide")

ensure_default_admin()

if not get_current_user():
    render_login()
    st.stop()

user = refresh_current_user()
if not user:
    render_login()
    st.stop()

if "page" not in st.session_state:
    st.session_state.page = "home"

PAGES = {
    "home": ("Home", render_home),
    "dashboard": ("Dashboard", render_dashboard),
    "data": ("Data Management", render_data_management),
    "admin": ("Admin Panel", render_admin),
}

if not can_access_page(user, st.session_state.page):
    st.session_state.page = "home"

with st.sidebar:
    st.title("Orion")
    st.caption(f"Signed in as **{user['display_name']}** ({user['role']})")
    if st.button("Sign out", use_container_width=True):
        logout()
        st.rerun()
    st.divider()

    for page_id, (label, _) in PAGES.items():
        if not can_access_page(user, page_id):
            continue
        if st.button(label, use_container_width=True, type="primary" if st.session_state.page == page_id else "secondary"):
            st.session_state.page = page_id
            st.rerun()

PAGES[st.session_state.page][1]()
