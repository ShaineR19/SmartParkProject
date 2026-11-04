
import streamlit as st
import pandas as pd


def show_dashboard():

    # Dashboard heading
    st.title("Dashboard")
    st.write("Welcome to Smart Park. Here's your parking overview.")
    st.divider()

    # Sample parking information
    total_spaces = 100
    available_spaces = 50
    assigned_spaces = 10
    occupied_spaces = 40
    current_vehicles = 40

    # Metric cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Spaces", total_spaces)

    with col2:
        st.metric("Available", available_spaces, delta="50%")

    with col3:
        st.metric("Assigned", assigned_spaces)

    with col4:
        st.metric("Occupied", occupied_spaces)

    st.write("")

    # Second section
    left_col, right_col = st.columns([2, 1])

    with left_col:
        st.subheader("Parking Overview")

        parking_data = pd.DataFrame({
            "Status": ["Available", "Assigned", "Occupied"],
            "Spaces": [available_spaces, assigned_spaces, occupied_spaces]
        })

        st.bar_chart(
            parking_data,
            x="Status",
            y="Spaces",
            color="#2878D0"
        )

    with right_col:
        st.subheader("Parking Summary")

        st.markdown(
            """
            <div style="
                background-color: white;
                padding: 20px;
                border-radius: 12px;
                border: 1px solid #E3E8F0;
                margin-bottom: 12px;
            ">
                <p style="color: #64748B; margin-bottom: 5px;">
                    Current Vehicles
                </p>
                <h2 style="color: #17243A; margin: 0;">
                    40
                </h2>
            </div>

            <div style="
                background-color: white;
                padding: 20px;
                border-radius: 12px;
                border: 1px solid #E3E8F0;
            ">
                <p style="color: #64748B; margin-bottom: 5px;">
                    Occupancy Rate
                </p>
                <h2 style="color="#52796F"; margin: 0;">
                    40%
                </h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")
    st.divider()

    # Parking status
    st.subheader("Parking Space Status")

    status_col1, status_col2, status_col3 = st.columns(3)

    with status_col1:
        st.success("Available")
        st.write("50 parking spaces")

    with status_col2:
        st.warning("Assigned")
        st.write("10 parking spaces")

    with status_col3:
        st.error("Occupied")
        st.write("40 parking spaces")

    st.caption("Smart Park Management System")
