"""Global CSS and reusable UI helpers for Orion."""

from textwrap import dedent
from typing import Optional

import streamlit as st


def _html(content: str) -> None:
    """Render HTML safely — content must not be indented (Markdown code-block rule)."""
    st.markdown(dedent(content).strip(), unsafe_allow_html=True)


_BACKGROUND_CSS = """
.orion-bg-layer {
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    overflow: hidden;
}

.orion-bg-grid {
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(36, 157, 143, 0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(233, 196, 106, 0.03) 1px, transparent 1px);
    background-size: 72px 72px;
    mask-image: radial-gradient(ellipse 80% 70% at 50% 30%, black 20%, transparent 75%);
    -webkit-mask-image: radial-gradient(ellipse 80% 70% at 50% 30%, black 20%, transparent 75%);
}

.orion-orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.55;
    animation: orion-float 18s ease-in-out infinite;
}

.orion-orb-1 {
    width: 520px;
    height: 520px;
    background: radial-gradient(circle, rgba(36, 157, 143, 0.4) 0%, transparent 70%);
    top: -12%;
    left: -8%;
    animation-delay: 0s;
}

.orion-orb-2 {
    width: 420px;
    height: 420px;
    background: radial-gradient(circle, rgba(233, 196, 106, 0.28) 0%, transparent 70%);
    top: 35%;
    right: -10%;
    animation-delay: -6s;
    animation-duration: 22s;
}

.orion-orb-3 {
    width: 380px;
    height: 380px;
    background: radial-gradient(circle, rgba(231, 111, 81, 0.3) 0%, transparent 70%);
    bottom: -8%;
    left: 25%;
    animation-delay: -12s;
    animation-duration: 20s;
}

.orion-orb-4 {
    width: 280px;
    height: 280px;
    background: radial-gradient(circle, rgba(253, 240, 213, 0.08) 0%, transparent 70%);
    top: 15%;
    left: 45%;
    animation-delay: -4s;
    animation-duration: 16s;
}

@keyframes orion-float {
    0%, 100% { transform: translate(0, 0) scale(1); }
    25% { transform: translate(40px, -30px) scale(1.06); }
    50% { transform: translate(-25px, 35px) scale(0.96); }
    75% { transform: translate(20px, 15px) scale(1.03); }
}

@keyframes orion-shimmer {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes orion-pulse-glow {
    0%, 100% { box-shadow: 0 0 20px rgba(36, 157, 143, 0.25); }
    50% { box-shadow: 0 0 40px rgba(36, 157, 143, 0.45); }
}
"""

_LOGIN_CSS = """
.orion-login-shell [data-testid="stVerticalBlockBorderWrapper"],
.main .block-container > div:first-child [data-testid="stVerticalBlockBorderWrapper"] {
    animation: orion-pulse-glow 4s ease-in-out infinite;
}
"""

_GLOBAL_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --orion-teal: #249D8F;
    --orion-gold: #E9C46A;
    --orion-coral: #E76F51;
    --orion-cream: #FDF0D5;
    --orion-primary: #249D8F;
    --orion-primary-light: #E9C46A;
    --orion-accent: #E76F51;
    --orion-surface: rgba(26, 32, 48, 0.85);
    --orion-surface-elevated: rgba(30, 36, 52, 0.75);
    --orion-glass: rgba(26, 32, 48, 0.65);
    --orion-border: rgba(253, 240, 213, 0.12);
    --orion-border-bright: rgba(36, 157, 143, 0.45);
    --orion-text: #FDF0D5;
    --orion-text-muted: rgba(253, 240, 213, 0.62);
    --orion-success: #249D8F;
    --orion-radius: 14px;
    --orion-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
}

html, body, [class*="css"] {
    font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
}

.stApp {
    background: #141820 !important;
}

[data-testid="stAppViewContainer"] {
    background: transparent !important;
}

[data-testid="stAppViewContainer"] > .main {
    background: transparent !important;
    z-index: 1;
}

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 1280px !important;
    position: relative;
    z-index: 1;
}

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent !important; }

/* Sidebar — frosted glass */
[data-testid="stSidebar"] {
    background: rgba(10, 15, 28, 0.82) !important;
    backdrop-filter: blur(24px) saturate(1.4) !important;
    -webkit-backdrop-filter: blur(24px) saturate(1.4) !important;
    border-right: 1px solid var(--orion-border) !important;
    box-shadow: 4px 0 24px rgba(0, 0, 0, 0.2) !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem !important;
}

.orion-brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.25rem 0 1.5rem 0;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid var(--orion-border);
}

.orion-brand-icon {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    background: linear-gradient(135deg, #249D8F, #E9C46A, #E76F51);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    font-weight: 700;
    color: #1a1f24;
    box-shadow: 0 4px 16px rgba(36, 157, 143, 0.35);
}

.orion-brand-text {
    font-size: 1.35rem;
    font-weight: 700;
    background: linear-gradient(135deg, #FDF0D5 0%, #E9C46A 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.02em;
}

.orion-user-card {
    background: var(--orion-glass);
    backdrop-filter: blur(12px);
    border: 1px solid var(--orion-border);
    border-radius: var(--orion-radius);
    padding: 0.875rem 1rem;
    margin-bottom: 1rem;
}

.orion-user-avatar {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: linear-gradient(135deg, #249D8F, #E9C46A);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.85rem;
    color: #1a1f24;
    margin-bottom: 0.5rem;
}

.orion-user-name {
    font-weight: 600;
    color: var(--orion-text);
    font-size: 0.9rem;
}

.orion-user-role {
    font-size: 0.72rem;
    color: var(--orion-gold);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.15rem;
    font-weight: 500;
}

/* Hero banner */
.orion-hero {
    position: relative;
    border-radius: 20px;
    padding: 2.25rem 2.5rem;
    margin-bottom: 2rem;
    overflow: hidden;
    border: 1px solid var(--orion-border);
    background: linear-gradient(135deg, rgba(36,157,143,0.12) 0%, rgba(233,196,106,0.06) 50%, rgba(231,111,81,0.08) 100%);
    backdrop-filter: blur(16px);
    box-shadow: var(--orion-shadow);
}

.orion-hero::before {
    content: '';
    position: absolute;
    top: -60%;
    right: -15%;
    width: 340px;
    height: 340px;
    background: radial-gradient(circle, rgba(99,102,241,0.25) 0%, transparent 65%);
    border-radius: 50%;
    pointer-events: none;
}

.orion-hero::after {
    content: '';
    position: absolute;
    bottom: -40%;
    left: 10%;
    width: 260px;
    height: 260px;
    background: radial-gradient(circle, rgba(34,211,238,0.15) 0%, transparent 65%);
    border-radius: 50%;
    pointer-events: none;
}

.orion-hero-content {
    position: relative;
    z-index: 1;
}

.orion-hero-greeting {
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--orion-teal);
    margin: 0 0 0.5rem 0;
}

.orion-hero-title {
    font-size: 2rem;
    font-weight: 700;
    color: var(--orion-text);
    letter-spacing: -0.03em;
    margin: 0 0 0.5rem 0;
    line-height: 1.15;
}

.orion-hero-subtitle {
    font-size: 1rem;
    color: var(--orion-text-muted);
    margin: 0;
    max-width: 520px;
    line-height: 1.6;
}

.orion-stat-strip {
    display: flex;
    gap: 1.5rem;
    flex-wrap: wrap;
    margin-top: 1.75rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--orion-border);
}

.orion-stat-item {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
}

.orion-stat-value {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--orion-text);
}

.orion-stat-label {
    font-size: 0.72rem;
    color: var(--orion-text-muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

/* Page headers */
.orion-page-header {
    margin-bottom: 2rem;
}

.orion-page-header-block {
    margin-bottom: 2rem;
}

.orion-page-eyebrow {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin: 0 0 0.5rem 0;
}

.orion-page-title {
    font-size: 1.85rem;
    font-weight: 700;
    color: #FDF0D5;
    letter-spacing: -0.03em;
    margin: 0 0 0.35rem 0;
    line-height: 1.15;
}

.orion-page-subtitle {
    font-size: 0.95rem;
    color: var(--orion-text-muted);
    margin: 0;
    line-height: 1.55;
}

.orion-panel-heading {
    margin: 0 0 1rem 0;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--orion-border);
}

.orion-panel-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--orion-text);
    margin: 0 0 0.2rem 0;
}

.orion-panel-subtitle {
    font-size: 0.8rem;
    color: var(--orion-text-muted);
    margin: 0;
}

.orion-kv-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 0.65rem 1.25rem;
    margin-bottom: 0.5rem;
}

.orion-kv-row {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
}

.orion-kv-key {
    font-size: 0.68rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--orion-text-muted);
}

.orion-kv-val {
    font-size: 0.875rem;
    color: var(--orion-text);
    word-break: break-word;
}

.orion-profile-card {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem 1.5rem;
    padding: 0.25rem 0;
}

.orion-profile-field-label {
    font-size: 0.68rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--orion-text-muted);
    margin-bottom: 0.2rem;
}

.orion-profile-field-value {
    font-size: 0.925rem;
    font-weight: 500;
    color: var(--orion-text);
}

.orion-status-active {
    color: #249D8F !important;
}

.orion-status-disabled {
    color: #F87171 !important;
}

.orion-danger-title {
    font-size: 0.9rem;
    font-weight: 600;
    color: #F87171;
    margin: 0 0 0.75rem 0;
}

/* Form inputs */
.stTextInput input,
.stNumberInput input,
.stDateInput input,
textarea {
    background: rgba(15, 23, 42, 0.7) !important;
    border: 1px solid var(--orion-border) !important;
    border-radius: 10px !important;
    color: var(--orion-text) !important;
}

.stTextInput input:focus,
.stNumberInput input:focus {
    border-color: var(--orion-primary) !important;
    box-shadow: 0 0 0 2px rgba(36, 157, 143, 0.2) !important;
}

[data-testid="stForm"] {
    border: none !important;
    padding: 0 !important;
}

[data-testid="stForm"] .stFormSubmitButton button {
    margin-top: 0.5rem !important;
}

.stCheckbox label span {
    color: var(--orion-text-muted) !important;
    font-size: 0.875rem !important;
}

/* Horizontal action radio — pill style */
.stRadio > div[role="radiogroup"] {
    gap: 0.5rem !important;
    flex-wrap: wrap !important;
}

.stRadio > div[role="radiogroup"] label {
    background: rgba(15, 23, 42, 0.55) !important;
    border: 1px solid var(--orion-border) !important;
    border-radius: 10px !important;
    padding: 0.45rem 1rem !important;
    margin: 0 !important;
    transition: all 0.15s ease !important;
}

.stRadio > div[role="radiogroup"] label:hover {
    border-color: var(--orion-border-bright) !important;
}

.stRadio > div[role="radiogroup"] label[data-checked="true"],
.stRadio > div[role="radiogroup"] label:has(input:checked) {
    background: rgba(36, 157, 143, 0.18) !important;
    border-color: rgba(36, 157, 143, 0.45) !important;
}

/* Bordered panels — consistent padding */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(15, 23, 42, 0.72) !important;
    backdrop-filter: blur(16px) !important;
    border: 1px solid var(--orion-border) !important;
    border-radius: 16px !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.22) !important;
    padding: 1.2rem 1.35rem !important;
}

/* Launch cards override padding */
div:has(.orion-launch-card-marker)[data-testid="stVerticalBlockBorderWrapper"] {
    padding: 0 !important;
    background: #1a2030 !important;
}

.orion-section-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--orion-text);
    margin: 0 0 1rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.orion-section-title::before {
    content: '';
    display: inline-block;
    width: 3px;
    height: 1em;
    background: linear-gradient(180deg, #249D8F, #E9C46A);
    border-radius: 2px;
}

/* Metric cards — glass with gradient border */
.orion-metric-card {
    background: var(--orion-glass);
    backdrop-filter: blur(16px);
    border: 1px solid var(--orion-border);
    border-radius: var(--orion-radius);
    padding: 1.2rem 1.3rem;
    transition: border-color 0.25s ease, transform 0.25s ease, box-shadow 0.25s ease;
    position: relative;
    overflow: hidden;
}

.orion-metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, #249D8F, #E9C46A, #E76F51);
    opacity: 0;
    transition: opacity 0.25s ease;
}

.orion-metric-card:hover {
    border-color: rgba(36, 157, 143, 0.4) !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(36, 157, 143, 0.12);
}

.orion-metric-card:hover::before {
    opacity: 1;
}

.orion-metric-label {
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--orion-text-muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.4rem;
}

.orion-metric-value {
    font-size: 1.55rem;
    font-weight: 700;
    color: var(--orion-text);
    letter-spacing: -0.02em;
    line-height: 1.2;
}

.orion-metric-delta {
    font-size: 0.78rem;
    font-weight: 600;
    margin-top: 0.3rem;
    padding: 0.15rem 0.5rem;
    border-radius: 6px;
    display: inline-block;
}

.orion-metric-delta.positive {
    color: #249D8F;
    background: rgba(36, 157, 143, 0.14);
}
.orion-metric-delta.negative {
    color: #F87171;
    background: rgba(248, 113, 113, 0.12);
}
.orion-metric-delta.neutral {
    color: var(--orion-text-muted);
    background: rgba(253, 240, 213, 0.08);
}

/* Glass chart panel wrapper */
.orion-chart-panel {
    background: var(--orion-glass);
    backdrop-filter: blur(16px);
    border: 1px solid var(--orion-border);
    border-radius: var(--orion-radius);
    padding: 0.5rem 0.75rem 0.75rem;
    margin-bottom: 0.5rem;
}

/* Login */
.orion-login-brand {
    text-align: center;
    padding: 1.5rem 1rem 0.5rem;
}

.orion-login-logo {
    width: 64px;
    height: 64px;
    border-radius: 18px;
    background: linear-gradient(135deg, #249D8F, #E9C46A, #E76F51);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 1.65rem;
    font-weight: 700;
    color: #1a1f24;
    box-shadow: 0 12px 32px rgba(36, 157, 143, 0.35);
    margin-bottom: 1.25rem;
}

.orion-login-title {
    font-size: 1.85rem;
    font-weight: 700;
    background: linear-gradient(135deg, #FDF0D5, #E9C46A);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.03em;
    margin: 0;
}

.orion-login-subtitle {
    color: var(--orion-text-muted);
    font-size: 0.95rem;
    margin-top: 0.4rem;
}

.orion-login-footer {
    text-align: center;
    font-size: 0.75rem;
    color: var(--orion-text-muted);
    margin-top: 1.5rem;
    opacity: 0.7;
}

/* Buttons — default primary uses brand gradient */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #249D8F, #1d7f74) !important;
    border: none !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease, opacity 0.15s ease !important;
    box-shadow: 0 4px 14px rgba(36, 157, 143, 0.35) !important;
    color: #ffffff !important;
}

.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(36, 157, 143, 0.4) !important;
}

.stButton > button[kind="secondary"] {
    background: var(--orion-glass) !important;
    backdrop-filter: blur(8px) !important;
    border: 1px solid var(--orion-border) !important;
    color: var(--orion-text) !important;
    font-weight: 500 !important;
    border-radius: 10px !important;
}

.stButton > button[kind="secondary"]:hover {
    border-color: var(--orion-border-bright) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.25rem;
    background: var(--orion-glass);
    backdrop-filter: blur(12px);
    border: 1px solid var(--orion-border);
    border-radius: 12px;
    padding: 0.35rem;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    font-weight: 500;
    padding: 0.5rem 1rem;
}

.stTabs [aria-selected="true"] {
    background: rgba(36, 157, 143, 0.2) !important;
}

/* Dataframes */
[data-testid="stDataFrame"] {
    border: 1px solid var(--orion-border);
    border-radius: var(--orion-radius);
    overflow: hidden;
    background: var(--orion-glass);
}

hr {
    border-color: var(--orion-border) !important;
    margin: 1.5rem 0 !important;
}

.stRadio > label, .stSelectbox > label {
    font-weight: 500 !important;
    color: var(--orion-text-muted) !important;
    font-size: 0.85rem !important;
}

/* Plotly charts sit inside glass feel */
[data-testid="stPlotlyChart"] {
    border-radius: var(--orion-radius);
    overflow: hidden;
}
"""


def _inject_css(*parts: str):
    css = "\n".join(parts)
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_background(intense: bool = False):
    """Inject animated mesh background with floating orbs and grid."""
    extra_orb = '<div class="orion-orb orion-orb-4"></div>' if intense else ""
    _html(f"""
    <div class="orion-bg-layer">
    <div class="orion-bg-grid"></div>
    <div class="orion-orb orion-orb-1"></div>
    <div class="orion-orb orion-orb-2"></div>
    <div class="orion-orb orion-orb-3"></div>
    {extra_orb}
    </div>
    """)


def inject_global_styles(intense_background: bool = False):
    _inject_css(_BACKGROUND_CSS, _GLOBAL_CSS, _LOGIN_CSS)
    render_background(intense=intense_background)


def render_brand():
    _html("""
    <div class="orion-brand">
    <div class="orion-brand-icon">O</div>
    <div class="orion-brand-text">Orion</div>
    </div>
    """)


def render_user_card(display_name: str, role: str):
    from html import escape

    safe_name = escape(display_name or "")
    safe_role = escape(role or "")
    initial = (display_name or "?").strip()[:1].upper() or "?"
    _html(f"""
    <div class="orion-user-card">
    <div class="orion-user-avatar">{escape(initial)}</div>
    <div class="orion-user-name">{safe_name}</div>
    <div class="orion-user-role">{safe_role}</div>
    </div>
    """)


def render_hero(greeting: str, title: str, subtitle: str, stats: Optional[list] = None):
    stats_html = ""
    if stats:
        items = "".join(
            f'<div class="orion-stat-item"><span class="orion-stat-value">{val}</span>'
            f'<span class="orion-stat-label">{label}</span></div>'
            for val, label in stats
        )
        stats_html = f'<div class="orion-stat-strip">{items}</div>'

    _html(f"""
    <div class="orion-hero">
    <div class="orion-hero-content">
    <p class="orion-hero-greeting">{greeting}</p>
    <h1 class="orion-hero-title">{title}</h1>
    <p class="orion-hero-subtitle">{subtitle}</p>
    {stats_html}
    </div>
    </div>
    """)


def inject_page_theme(theme_key: str):
    from ui.theme import PAGE_BUTTON_TEXT, PAGE_GRADIENTS, page_shadow
    from ui.theme import PAGE_COLORS

    gradient = PAGE_GRADIENTS.get(theme_key, PAGE_GRADIENTS["default"])
    text_color = PAGE_BUTTON_TEXT.get(theme_key, "#ffffff")
    color = PAGE_COLORS.get(theme_key, PAGE_COLORS["default"])
    shadow = page_shadow(color)

    st.markdown(
        f"""
        <style>
        .main .block-container .stButton > button[kind="primary"],
        .main .block-container .stFormSubmitButton > button {{
            background: {gradient} !important;
            color: {text_color} !important;
            box-shadow: {shadow} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(title: str, subtitle: str = "", theme_key: str = "default"):
    from html import escape

    from ui.theme import PAGE_COLORS, PAGE_EYEBROWS

    inject_page_theme(theme_key)
    eyebrow = PAGE_EYEBROWS.get(theme_key, PAGE_EYEBROWS["default"])
    accent = PAGE_COLORS.get(theme_key, PAGE_COLORS["default"])
    subtitle_html = f'<p class="orion-page-subtitle">{escape(subtitle)}</p>' if subtitle else ""
    _html(f"""
    <div class="orion-page-header-block">
    <p class="orion-page-eyebrow" style="color:{accent};">{eyebrow}</p>
    <h1 class="orion-page-title">{escape(title)}</h1>
    {subtitle_html}
    </div>
    """)


def page_header(title: str, subtitle: str = "", theme_key: str = "default"):
    render_page_header(title, subtitle, theme_key)


def panel_header(title: str, subtitle: str = ""):
    from html import escape

    subtitle_html = f'<p class="orion-panel-subtitle">{escape(subtitle)}</p>' if subtitle else ""
    _html(f"""
    <div class="orion-panel-heading">
    <p class="orion-panel-title">{escape(title)}</p>
    {subtitle_html}
    </div>
    """)


def render_profile_card(username: str, display_name: str, role: str, is_active: bool):
    from html import escape

    status_class = "orion-status-active" if is_active else "orion-status-disabled"
    status_label = "Active" if is_active else "Disabled"
    _html(f"""
    <div class="orion-profile-card">
    <div>
    <div class="orion-profile-field-label">Username</div>
    <div class="orion-profile-field-value">{escape(username)}</div>
    </div>
    <div>
    <div class="orion-profile-field-label">Display Name</div>
    <div class="orion-profile-field-value">{escape(display_name)}</div>
    </div>
    <div>
    <div class="orion-profile-field-label">Role</div>
    <div class="orion-profile-field-value">{escape(role)}</div>
    </div>
    <div>
    <div class="orion-profile-field-label">Status</div>
    <div class="orion-profile-field-value {status_class}">{status_label}</div>
    </div>
    </div>
    """)


def render_kv_preview(record: dict):
    from html import escape

    if not record:
        return
    rows = "".join(
        f'<div class="orion-kv-row"><span class="orion-kv-key">{escape(str(k))}</span>'
        f'<span class="orion-kv-val">{escape(str(v))}</span></div>'
        for k, v in record.items()
    )
    _html(f'<div class="orion-kv-grid">{rows}</div>')


def render_danger_header(title: str = "Danger zone"):
    from html import escape

    _html(f'<p class="orion-danger-title">{escape(title)}</p>')


def section_title(title: str):
    from html import escape

    st.markdown(f'<p class="orion-section-title">{escape(title)}</p>', unsafe_allow_html=True)


def render_metric_card(label: str, value: str, delta: str = "", delta_type: str = "neutral"):
    from html import escape

    delta_html = ""
    if delta:
        delta_html = f'<div class="orion-metric-delta {escape(delta_type)}">{escape(delta)}</div>'
    _html(f"""
    <div class="orion-metric-card">
    <div class="orion-metric-label">{escape(label)}</div>
    <div class="orion-metric-value">{escape(value)}</div>
    {delta_html}
    </div>
    """)


def render_login_branding():
    _html("""
    <div class="orion-login-brand">
    <div class="orion-login-logo">O</div>
    <h1 class="orion-login-title">Welcome to Orion</h1>
    <p class="orion-login-subtitle">Your command center for business intelligence</p>
    </div>
    """)


def render_login_footer():
    st.markdown(
        '<p class="orion-login-footer">Secured workspace · Orion Platform</p>',
        unsafe_allow_html=True,
    )


def back_button(label: str = "Back to Home"):
    return st.button(f"← {label}", type="secondary")
