
import streamlit as st

from backend.database import DatabaseManager
from backend.parking_service import ParkingService


def show_parking():

    st.title("Parking Management")
    st.write("View parking space availability and status.")
    st.divider()

    # Connect to the database
    db = DatabaseManager()
    db.initialize_database()

    parking_service = ParkingService(db)

    # Create 100 parking spaces if they do not exist
    spaces = parking_service.get_all_spaces()

    if len(spaces) == 0:

        letters = "ABCDEFGHIJ"

        for letter in letters:
            for number in range(1, 11):
                space_number = f"{letter}{number}"
                db.add_parking_space(space_number)

        spaces = parking_service.get_all_spaces()

    # Get parking information from the database
    available_spaces = parking_service.get_available_spaces()
    assigned_spaces = parking_service.get_assigned_spaces()
    occupied_spaces = parking_service.get_occupied_spaces()

    total_spaces = len(spaces)
    available = len(available_spaces)
    assigned = len(assigned_spaces)
    occupied = len(occupied_spaces)

    # Summary cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Spaces", total_spaces)

    with col2:
        st.metric("Available", available)

    with col3:
        st.metric("Assigned", assigned)

    with col4:
        st.metric("Occupied", occupied)

    st.divider()

    # Parking lot legend
    st.subheader("Parking Lot Layout")

    legend1, legend2, legend3 = st.columns(3)

    with legend1:
        st.markdown("🟢 **Available**")

    with legend2:
        st.markdown("🟡 **Assigned**")

    with legend3:
        st.markdown("🔴 **Occupied**")

    st.write("")

    # Display parking spaces from SQLite
    spaces_by_number = {
        space["space_number"]: space["status"]
        for space in spaces
    }

    letters = "ABCDEFGHIJ"

    for letter in letters:

        cols = st.columns(10)

        for number in range(1, 11):

            space_number = f"{letter}{number}"
            status = spaces_by_number.get(
                space_number, "AVAILABLE"
            )

            if status == "AVAILABLE":
                color = "#DCFCE7"
                text_color = "#166534"
                display_status = "Available"

            elif status == "ASSIGNED":
                color = "#FEF3C7"
                text_color = "#92400E"
                display_status = "Assigned"

            else:
                color = "#FEE2E2"
                text_color = "#991B1B"
                display_status = "Occupied"

            with cols[number - 1]:

                st.markdown(
                    f"""
                    <div style="
                        background-color: {color};
                        color: {text_color};
                        border-radius: 8px;
                        padding: 12px 2px;
                        text-align: center;
                        margin-bottom: 10px;
                        border: 1px solid #E2E8F0;
                    ">
                        <b>{space_number}</b>
                        <br>
                        <small>{display_status}</small>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.divider()

    st.caption("Smart Park Management System")
