
import streamlit as st
import pandas as pd

from backend.database import DatabaseManager
from backend.parking_service import ParkingService


def show_vehicles():

    # Page heading
    st.title("Vehicle Management")
    st.write("Register vehicles and manage vehicle information.")
    st.divider()

    # Connect to database
    db = DatabaseManager()
    db.initialize_database()

    parking_service = ParkingService(db)

    # Add vehicle_name column if it does not already exist
    with db.connect() as conn:

        columns = [
            column["name"]
            for column in conn.execute(
                "PRAGMA table_info(vehicles)"
            ).fetchall()
        ]

        if "vehicle_name" not in columns:
            conn.execute(
                "ALTER TABLE vehicles ADD COLUMN vehicle_name TEXT"
            )

    # Make sure all 100 parking spaces exist
    existing_spaces = parking_service.get_all_spaces()

    existing_space_numbers = {
        space["space_number"] for space in existing_spaces
    }

    letters = "ABCDEFGHIJ"

    for letter in letters:
        for number in range(1, 11):

            space_number = f"{letter}{number}"

            if space_number not in existing_space_numbers:
                db.add_parking_space(space_number)

    # Vehicle registration section
    st.subheader("Register a Vehicle")

    with st.container(border=True):

        with st.form("vehicle_form"):

            license_plate = st.text_input(
                "License Plate Number",
                placeholder="Example: ABC123"
            )

            vehicle_name = st.text_input(
                "Vehicle Make or Model",
                placeholder="Example: Toyota Camry"
            )

            submitted = st.form_submit_button(
                "Register Vehicle",
                use_container_width=True
            )

            if submitted:

                if not license_plate.strip():
                    st.error("Please enter a license plate number.")

                elif not vehicle_name.strip():
                    st.error("Please enter the vehicle make or model.")

                else:

                    try:

                        # Register vehicle and assign parking space
                        result = parking_service.register_vehicle(
                            license_plate.strip().upper()
                        )

                        # Save vehicle make/model in SQLite
                        with db.connect() as conn:

                            conn.execute(
                                """
                                UPDATE vehicles
                                SET vehicle_name = ?
                                WHERE license_plate = ?
                                """,
                                (
                                    vehicle_name.strip(),
                                    license_plate.strip().upper()
                                )
                            )

                            conn.commit()

                        st.success(
                            f"Vehicle registered successfully! "
                            f"Assigned space: {result['space_number']}"
                        )

                    except ValueError as error:
                        st.error(str(error))

    st.write("")
    st.divider()

    # Registered vehicles section
    st.subheader("Registered Vehicles")

    # Retrieve vehicle information from SQLite
    with db.connect() as conn:

        vehicle_data = pd.read_sql_query(
            """
            SELECT
                v.license_plate AS 'License Plate',
                COALESCE(v.vehicle_name, '') AS 'Vehicle',
                CASE
                    WHEN p.status = 'ASSIGNED' THEN 'Assigned'
                    WHEN p.status = 'OCCUPIED' THEN 'Occupied'
                    ELSE 'Registered'
                END AS 'Status'
            FROM vehicles v
            LEFT JOIN parking_sessions s
                ON v.vehicle_id = s.vehicle_id
                AND s.status = 'ACTIVE'
            LEFT JOIN parking_spaces p
                ON s.space_id = p.space_id
            ORDER BY v.license_plate
            """,
            conn
        )

    # Display vehicle count
    st.metric(
        "Total Registered Vehicles",
        len(vehicle_data)
    )

    if not vehicle_data.empty:

        st.dataframe(
            vehicle_data,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No vehicles have been registered yet.")

    st.caption("Smart Park Management System")
