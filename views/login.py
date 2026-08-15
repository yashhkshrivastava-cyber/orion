import streamlit as st

from services.auth_service import authenticate, login
from ui.styles import render_login_branding, render_login_footer


def render_login():
    _, center, _ = st.columns([1, 1.05, 1])

    with center:
        with st.container(border=True):
            render_login_branding()

            with st.form("login_form", clear_on_submit=False):
                username = st.text_input("Username", placeholder="Enter your username", autocomplete="username")
                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password",
                    autocomplete="current-password",
                )
                submitted = st.form_submit_button("Sign in to Orion", use_container_width=True, type="primary")

            render_login_footer()

        if submitted:
            if not username.strip() or not password:
                st.error("Enter both username and password.")
            else:
                user = authenticate(username, password)
                if user:
                    login(user)
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
