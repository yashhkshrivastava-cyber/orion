from datetime import datetime

import streamlit as st

from services.auth_service import can_access_page, get_current_user
from ui.launch import WORKSPACES, inject_launch_styles, render_launch_card, render_launch_intro


def _greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning"
    if hour < 17:
        return "Good afternoon"
    return "Good evening"


def _available_workspaces(user):
    return [ws for ws in WORKSPACES if can_access_page(user, ws["page_id"])]


def render_home():
    user = get_current_user()
    name = user.get("display_name") or user.get("username", "there")
    workspaces = _available_workspaces(user)

    if not workspaces:
        st.warning("No pages are available for your account.")
        return

    inject_launch_styles()
    render_launch_intro(_greeting(), name)

    count = len(workspaces)
    if count == 1:
        columns = st.columns([1, 1, 1])
        slots = [columns[1]]
    else:
        columns = st.columns(count, gap="large")
        slots = list(columns)

    for slot, workspace in zip(slots, workspaces):
        with slot:
            if render_launch_card(**workspace):
                st.session_state.page = workspace["page_id"]
                st.rerun()
