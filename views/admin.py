import pandas as pd
import streamlit as st

from services.auth_service import (
    ROLE_LABELS,
    ROLES,
    create_user,
    delete_user,
    get_current_user,
    list_users,
    refresh_current_user,
    set_user_active,
    update_user_password,
    update_user_role,
)


def _render_user_list():
    st.subheader("All Users")
    users = list_users()

    if not users:
        st.info("No users found.")
        return

    df = pd.DataFrame(users)
    df["status"] = df["is_active"].map({True: "Active", False: "Disabled"})
    df = df.rename(
        columns={
            "username": "Username",
            "display_name": "Display Name",
            "role": "Role",
            "status": "Status",
            "created_timestamp": "Created",
        }
    )
    st.dataframe(
        df[["Username", "Display Name", "Role", "Status", "Created"]],
        use_container_width=True,
        hide_index=True,
    )


def _render_create_user():
    st.subheader("Create User")

    with st.form("create_user_form", clear_on_submit=True):
        username = st.text_input("Username")
        display_name = st.text_input("Display Name")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ROLES, format_func=lambda r: ROLE_LABELS[r])
        submitted = st.form_submit_button("Create User", type="primary")

    if submitted:
        try:
            create_user(username, display_name, password, role)
            st.success(f"User '{username.strip()}' created.")
            st.rerun()
        except ValueError as exc:
            st.error(str(exc))


def _render_manage_user():
    st.subheader("Manage User")

    users = list_users()
    current_user = get_current_user()

    if not users:
        st.info("No users available.")
        return

    options = {
        f"{user['display_name']} ({user['username']}) — {user['role']}": user["id"]
        for user in users
    }
    selected_label = st.selectbox("Select User", list(options.keys()))
    selected_id = options[selected_label]
    selected_user = next(user for user in users if user["id"] == selected_id)
    is_self = selected_id == current_user["id"]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Username:** {selected_user['username']}")
        st.markdown(f"**Display Name:** {selected_user['display_name']}")
    with col2:
        st.markdown(f"**Role:** {selected_user['role']}")
        st.markdown(f"**Status:** {'Active' if selected_user['is_active'] else 'Disabled'}")

    st.divider()

    new_role = st.selectbox(
        "Change Role",
        ROLES,
        index=ROLES.index(selected_user["role"]),
        format_func=lambda r: ROLE_LABELS[r],
        key=f"role_{selected_id}",
    )

    if st.button("Update Role", key=f"update_role_{selected_id}"):
        try:
            update_user_role(selected_id, new_role, current_user["id"])
            if is_self:
                refresh_current_user()
            st.success("Role updated.")
            st.rerun()
        except ValueError as exc:
            st.error(str(exc))

    if selected_user["is_active"]:
        if st.button("Disable User", key=f"disable_{selected_id}"):
            try:
                set_user_active(selected_id, False, current_user["id"])
                st.success("User disabled.")
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))
    else:
        if st.button("Enable User", key=f"enable_{selected_id}"):
            try:
                set_user_active(selected_id, True, current_user["id"])
                st.success("User enabled.")
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))

    st.divider()
    st.markdown("**Reset Password**")

    with st.form(f"reset_password_{selected_id}"):
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submitted = st.form_submit_button("Reset Password")

    if submitted:
        if new_password != confirm_password:
            st.error("Passwords do not match.")
        else:
            try:
                update_user_password(selected_id, new_password)
                st.success("Password updated.")
            except ValueError as exc:
                st.error(str(exc))

    st.divider()

    confirm_delete = st.checkbox("I confirm permanent deletion", key=f"confirm_delete_{selected_id}")
    if st.button("Delete User", key=f"delete_{selected_id}"):
        if not confirm_delete:
            st.warning("Please confirm deletion.")
        else:
            try:
                delete_user(selected_id, current_user["id"])
                st.success("User deleted.")
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))


def render_admin():
    if st.button("⬅️ Back"):
        st.session_state.page = "home"
        st.rerun()

    st.title("Admin Panel")
    st.caption("Manage users, roles, and access.")

    tab_users, tab_create, tab_manage = st.tabs(["Users", "Create User", "Manage User"])

    with tab_users:
        _render_user_list()

    with tab_create:
        _render_create_user()

    with tab_manage:
        _render_manage_user()
