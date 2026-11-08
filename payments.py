
import streamlit as st
import pandas as pd

from backend.database import DatabaseManager
from backend.parking_service import ParkingService


def show_payments():

    st.title("Payment Management")
    st.write("Calculate parking fees and manage completed payments.")
    st.divider()

    # Connect to active database
    db = DatabaseManager()
    db.initialize_database()

    parking_service = ParkingService(db)

    hourly_rate = 5.00

    # Get active vehicles
    active_vehicles = parking_service.get_active_vehicles()

    st.subheader("Process Vehicle Exit")

    with st.container(border=True):

        st.write("**Parking Information**")

        if active_vehicles:

            active_plates = [
                vehicle["license_plate"]
                for vehicle in active_vehicles
            ]

            license_plate = st.selectbox(
                "Select Vehicle License Plate",
                active_plates
            )

            selected_vehicle = next(
                vehicle for vehicle in active_vehicles
                if vehicle["license_plate"] == license_plate
            )

            st.write(
                f"Assigned Parking Space: "
                f"**{selected_vehicle['space_number']}**"
            )

            parking_hours = st.number_input(
                "Parking Duration (hours)",
                min_value=0.5,
                step=0.5,
                value=1.0
            )

            parking_fee = parking_hours * hourly_rate

            st.divider()

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Hourly Rate", f"${hourly_rate:.2f}")

            with col2:
                st.metric("Total Parking Fee", f"${parking_fee:.2f}")

            if st.button(
                "Complete Payment",
                use_container_width=True
            ):

                try:
                    # Complete checkout and release parking space
                    result = parking_service.checkout_vehicle(
                        license_plate,
                        hourly_rate,
                        parking_hours
                    )

                    st.success("Payment completed successfully!")

                    st.write("### Payment Receipt")

                    st.write(
                        f"**Transaction ID:** "
                        f"{result['transaction_id']}"
                    )

                    st.write(
                        f"**License Plate:** "
                        f"{result['license_plate']}"
                    )

                    st.write(
                        f"**Parking Space:** "
                        f"{result['space_number']}"
                    )

                    st.write(
                        f"**Parking Duration:** "
                        f"{result['duration_hours']:.2f} hours"
                    )

                    st.write(
                        f"**Amount Paid:** "
                        f"${result['payment_amount']:.2f}"
                    )

                    st.info(
                        f"Parking space {result['space_number']} "
                        "is now available."
                    )

                    st.rerun()

                except ValueError as error:
                    st.error(str(error))

        else:
            st.info("There are no active vehicles to check out.")

    st.divider()

    # Payment history from SQLite
    st.subheader("Payment History")

    transactions = parking_service.get_transactions()

    if transactions:

        payment_data = pd.DataFrame(transactions)

        total_transactions = len(payment_data)

        total_revenue = sum(
            transaction["payment_amount"]
            for transaction in transactions
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total Transactions", total_transactions)

        with col2:
            st.metric("Total Revenue", f"${total_revenue:.2f}")

        payment_data = payment_data.rename(columns={
            "transaction_id": "Transaction ID",
            "license_plate": "License Plate",
            "space_number": "Parking Space",
            "entry_time": "Entry Time",
            "exit_time": "Exit Time",
            "parking_duration": "Duration (Hours)",
            "payment_amount": "Parking Fee",
            "completed_at": "Completed At"
        })

        payment_data["Parking Fee"] = payment_data[
            "Parking Fee"
        ].apply(lambda amount: f"${amount:.2f}")

        st.dataframe(
            payment_data,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No payments have been completed yet.")

    st.caption("Smart Park Management System")
