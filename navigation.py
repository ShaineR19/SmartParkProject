
import streamlit as st


def navigation():

    # Sidebar heading
    st.sidebar.markdown(
        """
        <div style="padding: 15px;">
            <h2 style="color: #17243A; margin-bottom: 0">
                🅿️ Smart Park
            </h2>
            <p style="color: #64748B; font-size: 13px;">
                Parking Management System
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.divider()

    # Navigation menu
    selected_page = st.sidebar.radio(
        "MAIN MENU",
        [
            "Home",
            "Parking",
            "Map",
            "Vehicles",
            "Payments",
            "Reports"
        ],
        index=0,
        key="main_navigation"
    )

    st.sidebar.divider()

    st.sidebar.caption("Smart Park Management System")

    return selected_page
