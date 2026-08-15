"""Launch screen — image-first workspace gallery."""

from html import escape
from pathlib import Path
from textwrap import dedent

import streamlit as st

from ui.theme import CREAM, PAGE_COLORS, PAGE_EYEBROWS, PAGE_GRADIENTS, PAGE_BUTTON_TEXT, WORKSPACE_META

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets" / "workspaces"

WORKSPACES = [
    {
        "page_id": "dashboard",
        "title": WORKSPACE_META["dashboard"]["title"],
        "tagline": PAGE_EYEBROWS["dashboard"],
        "description": WORKSPACE_META["dashboard"]["description"],
        "image_name": "dashboard.png",
        "accent": PAGE_COLORS["dashboard"],
    },
    {
        "page_id": "data",
        "title": WORKSPACE_META["data"]["title"],
        "tagline": PAGE_EYEBROWS["data"],
        "description": WORKSPACE_META["data"]["description"],
        "image_name": "data.png",
        "accent": PAGE_COLORS["data"],
    },
    {
        "page_id": "admin",
        "title": WORKSPACE_META["admin"]["title"],
        "tagline": PAGE_EYEBROWS["admin"],
        "description": WORKSPACE_META["admin"]["description"],
        "image_name": "admin.png",
        "accent": PAGE_COLORS["admin"],
    },
]

_LAUNCH_CSS = """
.orion-launch-shell {
    max-width: 1120px;
    margin: 0 auto;
    padding: 0.5rem 0 2rem;
}

.orion-launch-intro {
    text-align: center;
    margin: 0.5rem 0 2.75rem;
}

.orion-launch-eyebrow {
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #249D8F;
    margin-bottom: 0.85rem;
}

.orion-launch-headline {
    font-size: clamp(1.85rem, 3vw, 2.35rem);
    font-weight: 700;
    color: #FDF0D5;
    letter-spacing: -0.035em;
    margin: 0 0 0.55rem 0;
    line-height: 1.12;
}

.orion-launch-lead {
    font-size: 1.02rem;
    color: rgba(253, 240, 213, 0.62);
    margin: 0;
    line-height: 1.55;
}

.main [data-testid="stHorizontalBlock"]:has(.orion-launch-card-marker) {
    align-items: stretch !important;
}

.main [data-testid="stHorizontalBlock"]:has(.orion-launch-card-marker) [data-testid="column"] {
    display: flex !important;
    flex-direction: column !important;
}

div:has(.orion-launch-card-marker)[data-testid="stVerticalBlockBorderWrapper"] {
    flex: 1 1 auto !important;
    display: flex !important;
    flex-direction: column !important;
    min-height: 400px !important;
    height: 100% !important;
    padding: 0 !important;
    overflow: hidden !important;
    border-radius: 20px !important;
    border: 1px solid rgba(253, 240, 213, 0.1) !important;
    background: #1a2030 !important;
    box-shadow: 0 16px 48px rgba(0, 0, 0, 0.28) !important;
    transition: transform 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease !important;
}

div:has(.orion-launch-card-marker[data-page="dashboard"])[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-4px);
    border-color: rgba(36, 157, 143, 0.55) !important;
    box-shadow: 0 22px 56px rgba(36, 157, 143, 0.15) !important;
}

div:has(.orion-launch-card-marker[data-page="data"])[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-4px);
    border-color: rgba(233, 196, 106, 0.55) !important;
    box-shadow: 0 22px 56px rgba(233, 196, 106, 0.12) !important;
}

div:has(.orion-launch-card-marker[data-page="admin"])[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-4px);
    border-color: rgba(231, 111, 81, 0.55) !important;
    box-shadow: 0 22px 56px rgba(231, 111, 81, 0.15) !important;
}

div:has(.orion-launch-card-marker) [data-testid="stImage"] {
    margin: 0 !important;
    padding: 0 !important;
    flex-shrink: 0 !important;
}

div:has(.orion-launch-card-marker) [data-testid="stImage"] img {
    width: 100% !important;
    height: 160px !important;
    min-height: 160px !important;
    max-height: 160px !important;
    object-fit: cover !important;
    display: block !important;
    border-radius: 0 !important;
}

.orion-launch-card-body {
    flex: 1 1 auto !important;
    display: flex !important;
    flex-direction: column !important;
    padding: 1.15rem 1.25rem 0.5rem !important;
    min-height: 130px !important;
}

.orion-launch-card-tag {
    display: inline-block;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.45rem;
}

.orion-launch-card-title {
    font-size: 1.15rem;
    font-weight: 600;
    color: #FDF0D5;
    margin: 0 0 0.35rem 0;
    letter-spacing: -0.02em;
}

.orion-launch-card-desc {
    font-size: 0.84rem;
    color: rgba(253, 240, 213, 0.62);
    margin: 0;
    line-height: 1.55;
    flex: 1 1 auto;
    min-height: 4rem;
    max-height: 4rem;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
}

div:has(.orion-launch-card-marker) .stButton {
    padding: 0 1.15rem 1.15rem !important;
    margin-top: auto !important;
    flex-shrink: 0 !important;
}

div:has(.orion-launch-card-marker) .stButton > button {
    width: 100% !important;
    border-radius: 11px !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    padding: 0.62rem 1rem !important;
    border: none !important;
}

div:has(.orion-launch-card-marker[data-page="dashboard"]) .stButton > button {
    background: linear-gradient(135deg, #249D8F, #1d7f74) !important;
    color: #ffffff !important;
    box-shadow: 0 4px 14px rgba(36, 157, 143, 0.35) !important;
}

div:has(.orion-launch-card-marker[data-page="data"]) .stButton > button {
    background: linear-gradient(135deg, #E9C46A, #d4aa4a) !important;
    color: #1a1f24 !important;
    box-shadow: 0 4px 14px rgba(233, 196, 106, 0.35) !important;
}

div:has(.orion-launch-card-marker[data-page="admin"]) .stButton > button {
    background: linear-gradient(135deg, #E76F51, #c45e42) !important;
    color: #ffffff !important;
    box-shadow: 0 4px 14px rgba(231, 111, 81, 0.35) !important;
}

div:has(.orion-launch-card-marker) .stButton > button:hover {
    filter: brightness(1.06);
}
"""


def _html(content: str) -> None:
    st.markdown(dedent(content).strip(), unsafe_allow_html=True)


def inject_launch_styles():
    st.markdown(f"<style>{_LAUNCH_CSS}</style>", unsafe_allow_html=True)


def render_launch_intro(greeting: str, name: str):
    safe_name = escape(name)
    _html(f"""
    <div class="orion-launch-shell">
    <div class="orion-launch-intro">
    <div class="orion-launch-eyebrow">{PAGE_EYEBROWS['default']}</div>
    <h1 class="orion-launch-headline">{greeting}, {safe_name}</h1>
    <p class="orion-launch-lead">Select a workspace to get started.</p>
    </div>
    </div>
    """)


def render_launch_card(page_id: str, title: str, tagline: str, description: str, image_name: str, accent: str):
    """Render one image-first workspace card. Returns True when Enter is clicked."""
    image_path = ASSETS_DIR / image_name
    if not image_path.exists():
        st.error(f"Missing image: {image_name}")
        return False

    with st.container(border=True):
        _html(f'<div class="orion-launch-card-marker" data-page="{page_id}"></div>')
        st.image(str(image_path), use_container_width=True)
        _html(f"""
        <div class="orion-launch-card-body">
        <div class="orion-launch-card-tag" style="color:{accent};">{escape(tagline)}</div>
        <p class="orion-launch-card-title">{escape(title)}</p>
        <p class="orion-launch-card-desc">{escape(description)}</p>
        </div>
        """)
        return st.button(
            "Enter workspace",
            key=f"launch_{page_id}",
            use_container_width=True,
            type="primary",
        )
