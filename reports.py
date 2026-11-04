import streamlit as st
import pandas as pd

def show_reports():

    st.title("Parking Reports")
    st.write("View parking activity and revenue reports.")

    st.divider()

    #Sample parking information
    total_spaces = 100
    available_spaces = 50
    assigned_spaces = 10
    occupied_spaces = 40

    #Payment information
    if "payments" not in st.session_state:
        st.session_state.payments = []

    total_transactions = len(st.session_state.payments)

    total_revenue = sum(
        float(payment["Parking Fee"].replace("$", ""))
        for payment in st.session_state.payments
    )

    # Parking overview
    st.subheader("Parking Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Spaces", total_spaces)
    col2.metric("Available", available_spaces)
    col3.metric("Assigned", assigned_spaces)
    col4.metric("Occupied", occupied_spaces)

    st.divider()

    #Revenue overview
    st.subheader("Revenue Overview")

    col1, col2 = st.columns(2)

    col1.metric("Completed Payments", total_transactions)

    col2.metric("Total Revenue", f"${total_revenue:.2f}")

    st.divider()

    #Parking capacity chart
    st.subheader("Parking Space Status")

    parking_data = pd.DataFrame({
        "Status": ["Available", "Assigned", "Occupied"],
        "Spaces": [available_spaces,assigned_spaces,occupied_spaces]    
        
        })

    st.bar_chart(
            parking_data,
            x="Status",
            y="Spaces"
        )
    
    st.divider()

    #Revenue chart
    st.subheader("Revenue Report")

    if st.session_state.payments:

            revenue_data =pd.DataFrame(
                st.session_state.payments
            
            )

            revenue_data["Parking Fee"] = (
                revenue_data["Parking Fee"]
                .str.replace("$", "", regex=False)
                .astpe(float)

            )

            st.bar_chart(
                revenue_data,
                x="License Plate",
                y="Parking Fee"

            )
    else:
             st.info("No payment information available yet.")

    st.divider()

        #Transaction history
    st.subheader("Completed Transactions")

    if st.session_state.payments:

            st.dataframe(
                st.session_state.payments,
                use_container_width=True

            )
    else:
            st.info("No completed transactions available.")

    