
import streamlit as st
import pandas as pd


def show_payments():

    # Page heading
    st.title("Payment Management")
    st.write("Calculate parking fees and manage completed payments.")
    st.divider()

    # Initialize payment storage
    if "payments" not in st.session_state:
        st.session_state.payments = []

    # Parking rate
    hourly_rate = 5.00

    # Payment calculation
    st.subheader("Calculate Parking Fee")

    with st.container(border=True):

        st.write("**Parking Information**")

        license_plate = st.text_input(
            "License Plate Number",
            placeholder="Example: ABC123",
            key="payment_plate"
        )

        parking_hours = st.number_input(
            "Parking Duration (hours)",
            min_value=0.0,
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

        # Complete payment
        if st.button("Complete Payment", use_container_width=True):

            if not license_plate.strip():
                st.error("Please enter a license plate number.")

            elif parking_hours <= 0:
                st.error("Parking duration must be greater than zero.")

            else:

                payment = {
                    "License Plate": license_plate.strip().upper(),
                    "Parking Duration": parking_hours,
                    "Parking Fee": f"${parking_fee:.2f}",
                    "Payment Status": "Completed"
                }

                st.session_state.payments.append(payment)

                st.success("Payment completed successfully!")

    st.write("")
    st.divider()

    # Payment history
    st.subheader("Payment History")

    total_transactions = len(st.session_state.payments)

    total_revenue = sum(
        float(payment["Parking Fee"].replace("$", ""))
        for payment in st.session_state.payments
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Transactions", total_transactions)

    with col2:
        st.metric("Total Revenue", f"${total_revenue:.2f}")

    if st.session_state.payments:

        payment_data = pd.DataFrame(
            st.session_state.payments
        )

        st.dataframe(
            payment_data,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No payments have been completed yet.")

    st.caption("Smart Park Management System")
