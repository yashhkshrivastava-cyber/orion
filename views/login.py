from typing import Optional

import streamlit as st

from services.auth_service import authenticate, login
from ui.styles import render_login_branding, render_login_footer


def render_login() -> Optional[bool]:
    """Render the login screen.

    Returns:
        True  — user authenticated this run
        False — form submitted but credentials were invalid
        None  — form not submitted yet
    """
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

        if not submitted:
            return None

        if not username.strip() or not password:
            st.error("Enter both username and password.")
            return False

        user = authenticate(username, password)
        if user:
            login(user)
            return True

        st.error("Invalid username or password.")
        return False
