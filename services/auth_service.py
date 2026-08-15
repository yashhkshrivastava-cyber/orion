import os
import re
from typing import Dict, List, Optional

import bcrypt
import streamlit as st

from db.connection import get_connection

SESSION_USER_KEY = "auth_user"
APP_USER_TABLE = "orion_ods.app_user"

ROLES = ("admin", "editor", "viewer")

ROLE_PAGES = {
    "admin": {"home", "dashboard", "data", "admin"},
    "editor": {"home", "dashboard", "data"},
    "viewer": {"home", "dashboard"},
}

ROLE_LABELS = {
    "admin": "Admin — full access + user management",
    "editor": "Editor — dashboard and data management",
    "viewer": "Viewer — dashboard only",
}

USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9._-]{3,32}$")


def _env(name: str, default: str) -> str:
    return os.environ.get(name, default)


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())


def _row_to_user(row, columns):
    user = dict(zip(columns, row))
    user.pop("password_hash", None)
    return user


def _fetch_user_by_username(username: str):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            f"""
            SELECT id, username, display_name, password_hash, role, is_active
            FROM {APP_USER_TABLE}
            WHERE username = %s
            """,
            (username,),
        )
        row = cur.fetchone()
        if not row:
            return None
        cols = [desc[0] for desc in cur.description]
        return dict(zip(cols, row))
    finally:
        cur.close()
        conn.close()


def fetch_user_by_id(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            f"""
            SELECT id, username, display_name, role, is_active, created_timestamp
            FROM {APP_USER_TABLE}
            WHERE id = %s
            """,
            (user_id,),
        )
        row = cur.fetchone()
        if not row:
            return None
        cols = [desc[0] for desc in cur.description]
        return _row_to_user(row, cols)
    finally:
        cur.close()
        conn.close()


def list_users():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            f"""
            SELECT id, username, display_name, role, is_active, created_timestamp
            FROM {APP_USER_TABLE}
            ORDER BY username
            """
        )
        rows = cur.fetchall()
        cols = [desc[0] for desc in cur.description]
        return [_row_to_user(row, cols) for row in rows]
    finally:
        cur.close()
        conn.close()


def _user_count() -> int:
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT COUNT(*) FROM {APP_USER_TABLE}")
        return cur.fetchone()[0]
    finally:
        cur.close()
        conn.close()


def count_active_admins(exclude_user_id: Optional[int] = None) -> int:
    conn = get_connection()
    cur = conn.cursor()
    try:
        if exclude_user_id is None:
            cur.execute(
                f"""
                SELECT COUNT(*) FROM {APP_USER_TABLE}
                WHERE role = 'admin' AND is_active = TRUE
                """
            )
        else:
            cur.execute(
                f"""
                SELECT COUNT(*) FROM {APP_USER_TABLE}
                WHERE role = 'admin' AND is_active = TRUE AND id <> %s
                """,
                (exclude_user_id,),
            )
        return cur.fetchone()[0]
    finally:
        cur.close()
        conn.close()


def validate_username(username: str) -> Optional[str]:
    username = username.strip()
    if not USERNAME_PATTERN.match(username):
        return "Username must be 3-32 characters and use letters, numbers, dots, dashes, or underscores."
    return None


def validate_password(password: str) -> Optional[str]:
    if len(password) < 8:
        return "Password must be at least 8 characters."
    return None


def create_user(username: str, display_name: str, password: str, role: str = "viewer"):
    username = username.strip()
    display_name = display_name.strip()

    if role not in ROLES:
        raise ValueError("Invalid role.")
    if validate_username(username):
        raise ValueError(validate_username(username))
    if validate_password(password):
        raise ValueError(validate_password(password))
    if not display_name:
        raise ValueError("Display name is required.")
    if _fetch_user_by_username(username):
        raise ValueError("Username already exists.")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            f"""
            INSERT INTO {APP_USER_TABLE} (username, display_name, password_hash, role)
            VALUES (%s, %s, %s, %s)
            """,
            (username, display_name, hash_password(password), role),
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()


def update_user_role(user_id: int, role: str, acting_user_id: int):
    if role not in ROLES:
        raise ValueError("Invalid role.")

    target = fetch_user_by_id(user_id)
    if not target:
        raise ValueError("User not found.")
    if target["role"] == "admin" and role != "admin" and count_active_admins(exclude_user_id=user_id) == 0:
        raise ValueError("Cannot change role of the last active admin.")
    if user_id == acting_user_id and role != "admin":
        raise ValueError("You cannot remove your own admin access.")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            f"""
            UPDATE {APP_USER_TABLE}
            SET role = %s, updated_timestamp = CURRENT_TIMESTAMP
            WHERE id = %s
            """,
            (role, user_id),
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()


def set_user_active(user_id: int, is_active: bool, acting_user_id: int):
    target = fetch_user_by_id(user_id)
    if not target:
        raise ValueError("User not found.")
    if user_id == acting_user_id and not is_active:
        raise ValueError("You cannot disable your own account.")
    if target["role"] == "admin" and not is_active and count_active_admins(exclude_user_id=user_id) == 0:
        raise ValueError("Cannot disable the last active admin.")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            f"""
            UPDATE {APP_USER_TABLE}
            SET is_active = %s, updated_timestamp = CURRENT_TIMESTAMP
            WHERE id = %s
            """,
            (is_active, user_id),
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()


def update_user_password(user_id: int, password: str):
    if validate_password(password):
        raise ValueError(validate_password(password))

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            f"""
            UPDATE {APP_USER_TABLE}
            SET password_hash = %s, updated_timestamp = CURRENT_TIMESTAMP
            WHERE id = %s
            """,
            (hash_password(password), user_id),
        )
        if cur.rowcount == 0:
            raise ValueError("User not found.")
        conn.commit()
    finally:
        cur.close()
        conn.close()


def delete_user(user_id: int, acting_user_id: int):
    target = fetch_user_by_id(user_id)
    if not target:
        raise ValueError("User not found.")
    if user_id == acting_user_id:
        raise ValueError("You cannot delete your own account.")
    if target["role"] == "admin" and count_active_admins(exclude_user_id=user_id) == 0:
        raise ValueError("Cannot delete the last active admin.")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(f"DELETE FROM {APP_USER_TABLE} WHERE id = %s", (user_id,))
        conn.commit()
    finally:
        cur.close()
        conn.close()


def ensure_default_admin():
    """Create the first admin account when no users exist yet."""
    if _user_count() > 0:
        return

    username = _env("ORION_ADMIN_USERNAME", "admin")
    password = _env("ORION_ADMIN_PASSWORD", "orion_dev_password")
    create_user(username, username.title(), password, role="admin")


def authenticate(username: str, password: str):
    user = _fetch_user_by_username(username.strip())
    if not user or not user["is_active"]:
        return None
    if not verify_password(password, user["password_hash"]):
        return None

    return {
        "id": user["id"],
        "username": user["username"],
        "display_name": user["display_name"],
        "role": user["role"],
    }


def can_access_page(user: Optional[Dict], page_id: str) -> bool:
    if not user:
        return False
    return page_id in ROLE_PAGES.get(user["role"], set())


def is_admin(user: Optional[Dict]) -> bool:
    return bool(user and user.get("role") == "admin")


def login(user: dict):
    st.session_state[SESSION_USER_KEY] = user


def logout():
    st.session_state.pop(SESSION_USER_KEY, None)
    st.session_state.pop("page", None)


def get_current_user():
    return st.session_state.get(SESSION_USER_KEY)


def refresh_current_user():
    user = get_current_user()
    if not user:
        return None

    updated = fetch_user_by_id(user["id"])
    if not updated or not updated["is_active"]:
        logout()
        return None

    session_user = {
        "id": updated["id"],
        "username": updated["username"],
        "display_name": updated["display_name"],
        "role": updated["role"],
    }
    login(session_user)
    return session_user
