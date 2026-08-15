"""Shared panel and form layout helpers."""

from contextlib import contextmanager

import streamlit as st

from ui.styles import panel_header, section_title


@contextmanager
def orion_panel(title: str = "", subtitle: str = ""):
    with st.container(border=True):
        if title:
            panel_header(title, subtitle)
        yield


def action_selector(options, key: str = "orion_action"):
    section_title("Action")
    return st.radio(
        "Action",
        options,
        horizontal=True,
        label_visibility="collapsed",
        key=key,
    )
