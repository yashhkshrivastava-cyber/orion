import streamlit as st

from services.auth_service import authenticate, login


def render_login():
    st.markdown(
        """
        <style>
        .login-card {
            max-width: 420px;
            margin: 4rem auto 0 auto;
            padding: 2rem;
            border: 1px solid rgba(49, 51, 63, 0.2);
            border-radius: 0.75rem;
            background: rgba(255, 255, 255, 0.02);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    _, center, _ = st.columns([1, 1.2, 1])

    with center:
        st.title("Orion")
        st.caption("Sign in to access your workspace")

        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", autocomplete="username")
            password = st.text_input("Password", type="password", autocomplete="current-password")
            submitted = st.form_submit_button("Sign in", use_container_width=True, type="primary")

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
