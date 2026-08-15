import pandas as pd
import streamlit as st

from services.auth_service import (
    ROLE_DEFAULT_DATA_ACCESS,
    ROLE_LABELS,
    ROLES,
    create_user,
    delete_user,
    get_current_user,
    list_users,
    refresh_current_user,
    set_user_active,
    update_user_data_access,
    update_user_password,
    update_user_role,
)
from ui.panels import orion_panel
from ui.styles import back_button, page_header, render_danger_header, render_profile_card


def _render_user_list():
    with orion_panel("All users", "Overview of accounts on the platform"):
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
                "ods_access": "ODS",
                "dw_access": "DW",
                "created_timestamp": "Created",
            }
        )
        df["ODS"] = df["ODS"].map({True: "Yes", False: "—"})
        df["DW"] = df["DW"].map({True: "Yes", False: "—"})
        st.dataframe(
            df[["Username", "Display Name", "Role", "ODS", "DW", "Status", "Created"]],
            use_container_width=True,
            hide_index=True,
        )


def _render_create_user():
    with orion_panel("Create user", "Add a new account to the platform"):
        with st.form("create_user_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                username = st.text_input("Username", placeholder="jane.doe")
                display_name = st.text_input("Display name", placeholder="Jane Doe")
            with col2:
                password = st.text_input("Password", type="password", placeholder="Min. 8 characters")
                role = st.selectbox("Role", ROLES, format_func=lambda r: ROLE_LABELS[r])
            defaults = ROLE_DEFAULT_DATA_ACCESS[role]
            access_col1, access_col2 = st.columns(2)
            with access_col1:
                ods_access = st.checkbox("Operational database (ODS)", value=defaults[0])
            with access_col2:
                dw_access = st.checkbox("Data warehouse (DW)", value=defaults[1])
            submitted = st.form_submit_button("Create user", type="primary", use_container_width=True)

        if submitted:
            try:
                create_user(
                    username,
                    display_name,
                    password,
                    role,
                    ods_access=ods_access,
                    dw_access=dw_access,
                )
                st.success(f"User '{username.strip()}' created.")
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))


def _render_manage_user():
    users = list_users()
    current_user = get_current_user()

    if not users:
        st.info("No users available.")
        return

    options = {
        f"{user['display_name']} ({user['username']})": user["id"]
        for user in users
    }

    with orion_panel("Select user", "Choose an account to manage"):
        selected_label = st.selectbox("User", list(options.keys()), label_visibility="collapsed")
        selected_id = options[selected_label]
        selected_user = next(user for user in users if user["id"] == selected_id)
        is_self = selected_id == current_user["id"]

    with orion_panel("Account details"):
        render_profile_card(
            selected_user["username"],
            selected_user["display_name"],
            selected_user["role"],
            selected_user["is_active"],
        )

    with orion_panel("Role & status", "Update access level or enable/disable the account"):
        new_role = st.selectbox(
            "Role",
            ROLES,
            index=ROLES.index(selected_user["role"]),
            format_func=lambda r: ROLE_LABELS[r],
            key=f"role_{selected_id}",
        )

        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("Update role", key=f"update_role_{selected_id}", use_container_width=True, type="primary"):
                try:
                    update_user_role(selected_id, new_role, current_user["id"])
                    if is_self:
                        refresh_current_user()
                    st.success("Role updated.")
                    st.rerun()
                except ValueError as exc:
                    st.error(str(exc))

        with col2:
            if selected_user["is_active"]:
                if st.button("Disable", key=f"disable_{selected_id}", use_container_width=True):
                    try:
                        set_user_active(selected_id, False, current_user["id"])
                        st.success("User disabled.")
                        st.rerun()
                    except ValueError as exc:
                        st.error(str(exc))
            elif st.button("Enable", key=f"enable_{selected_id}", use_container_width=True):
                try:
                    set_user_active(selected_id, True, current_user["id"])
                    st.success("User enabled.")
                    st.rerun()
                except ValueError as exc:
                    st.error(str(exc))

    with orion_panel("Data access", "Control ODS and DW permissions independently of role"):
        ods_access = st.checkbox(
            "Operational database (ODS)",
            value=bool(selected_user.get("ods_access")),
            key=f"ods_access_{selected_id}",
        )
        dw_access = st.checkbox(
            "Data warehouse (DW)",
            value=bool(selected_user.get("dw_access")),
            key=f"dw_access_{selected_id}",
        )
        if st.button("Update data access", key=f"update_data_access_{selected_id}", use_container_width=True):
            try:
                update_user_data_access(selected_id, ods_access, dw_access, current_user["id"])
                if is_self:
                    refresh_current_user()
                st.success("Data access updated.")
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))

    with orion_panel("Reset password", "Set a new password for this account"):
        with st.form(f"reset_password_{selected_id}"):
            col1, col2 = st.columns(2)
            with col1:
                new_password = st.text_input("New password", type="password")
            with col2:
                confirm_password = st.text_input("Confirm password", type="password")
            submitted = st.form_submit_button("Update password", type="primary", use_container_width=True)

        if submitted:
            if new_password != confirm_password:
                st.error("Passwords do not match.")
            else:
                try:
                    update_user_password(selected_id, new_password)
                    st.success("Password updated.")
                except ValueError as exc:
                    st.error(str(exc))

    with orion_panel("Danger zone", "Irreversible actions"):
        render_danger_header("Delete this user permanently")
        confirm_delete = st.checkbox(
            "I confirm permanent deletion",
            key=f"confirm_delete_{selected_id}",
        )
        if st.button("Delete user", key=f"delete_{selected_id}", type="primary", use_container_width=True):
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
    if back_button():
        st.session_state.page = "home"
        st.rerun()

    page_header(
        "Admin Panel",
        "Manage users, roles, and platform access.",
        theme_key="admin",
    )

    tab_users, tab_create, tab_manage = st.tabs(["Users", "Create user", "Manage user"])

    with tab_users:
        _render_user_list()

    with tab_create:
        _render_create_user()

    with tab_manage:
        _render_manage_user()
