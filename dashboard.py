
import streamlit as st
from backend.database import DatabaseManager
from backend.parking_service import ParkingService


def show_dashboard():

    st.title("Dashboard")
    st.write("Welcome to Smart Park. Here's your parking overview.")
    st.divider()

    # Connect to the active SQLite database
    db = DatabaseManager()
    db.initialize_database()

    parking_service = ParkingService(db)

    # Get live parking information
    summary = parking_service.get_lot_summary()

    total_spaces = summary["total_spaces"] or 0
    available_spaces = summary["available_spaces"] or 0
    assigned_spaces = summary["assigned_spaces"] or 0
    occupied_spaces = summary["occupied_spaces"] or 0

    # Get active vehicles from the database
    active_vehicles = parking_service.get_active_vehicles()
    current_vehicles = len(active_vehicles)

    # Display dashboard metrics
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total Spaces", total_spaces)

    with col2:
        st.metric("Available", available_spaces)

    with col3:
        st.metric("Assigned", assigned_spaces)

    with col4:
        st.metric("Occupied", occupied_spaces)

    with col5:
        st.metric("Current Vehicles", current_vehicles)

    st.divider()

    # Parking space overview
    st.subheader("Parking Space Overview")

    chart_data = {
        "Status": ["Available", "Assigned", "Occupied"],
        "Spaces": [
            available_spaces,
            assigned_spaces,
            occupied_spaces
        ]
    }

    st.bar_chart(
        chart_data,
        x="Status",
        y="Spaces"
    )

    st.divider()

    # Active vehicles
    st.subheader("Currently Active Vehicles")

    if active_vehicles:

        st.dataframe(
            active_vehicles,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("There are currently no active vehicles.")
