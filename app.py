import streamlit as st

from services.auth_service import (
    can_access_page,
    ensure_default_admin,
    get_current_user,
    logout,
    refresh_current_user,
)
from ui.styles import inject_global_styles, render_brand, render_user_card
from views.admin import render_admin
from views.dashboard import render_dashboard
from views.data_management import render_data_management
from views.home import render_home
from views.login import render_login

st.set_page_config(
    page_title="Orion",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_styles(intense_background=True)
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
    render_brand()
    render_user_card(user["display_name"], user["role"])

    if st.button("Sign out", use_container_width=True, type="secondary"):
        logout()
        st.rerun()

    st.markdown("<div style='margin: 1rem 0; border-top: 1px solid rgba(148,163,184,0.12);'></div>", unsafe_allow_html=True)

    for page_id, (label, _) in PAGES.items():
        if not can_access_page(user, page_id):
            continue
        is_active = st.session_state.page == page_id
        if st.button(
            label,
            use_container_width=True,
            type="primary" if is_active else "secondary",
            key=f"nav_{page_id}",
        ):
            st.session_state.page = page_id
            st.rerun()

PAGES[st.session_state.page][1]()
