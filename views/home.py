import streamlit as st

from services.auth_service import can_access_page, get_current_user


def render_home():
    user = get_current_user()

    st.title("🚀 Orion Platform")
    st.markdown("### Choose where you want to go")

    cards = []

    if can_access_page(user, "dashboard"):
        cards.append(
            {
                "title": "📊 Dashboard",
                "description": "View KPIs, Revenue, Expense & Analytics",
                "color": "#1f77b4",
                "page": "dashboard",
                "label": "Open Dashboard",
            }
        )

    if can_access_page(user, "data"):
        cards.append(
            {
                "title": "🛠️ Data Management",
                "description": "Create, Update & Manage Data",
                "color": "#ff7f0e",
                "page": "data",
                "label": "Open Data Management",
            }
        )

    if can_access_page(user, "admin"):
        cards.append(
            {
                "title": "🛡️ Admin Panel",
                "description": "Manage users, roles, and access",
                "color": "#2ca02c",
                "page": "admin",
                "label": "Open Admin Panel",
            }
        )

    if not cards:
        st.warning("No pages are available for your account.")
        return

    columns = st.columns(len(cards))

    for column, card in zip(columns, cards):
        with column:
            st.markdown(
                f"""
                <div style="padding:30px;border-radius:15px;background-color:{card['color']};color:white;text-align:center">
                    <h2>{card['title']}</h2>
                    <p>{card['description']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button(card["label"], key=f"open_{card['page']}"):
                st.session_state.page = card["page"]
                st.rerun()
