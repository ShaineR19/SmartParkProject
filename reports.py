
import streamlit as st
import pandas as pd

from backend.database import DatabaseManager


def show_reports():

    st.title("Parking Reports")
    st.write("View parking activity and revenue reports.")

    st.divider()

    # Connect to SQLite database
    db = DatabaseManager()
    db.initialize_database()

    # Retrieve parking and payment information
    with db.connect() as conn:

        # Parking space counts
        parking_counts = conn.execute("""
            SELECT
                COUNT(*) AS total_spaces,
                SUM(CASE WHEN status = 'AVAILABLE' THEN 1 ELSE 0 END) AS available,
                SUM(CASE WHEN status = 'ASSIGNED' THEN 1 ELSE 0 END) AS assigned,
                SUM(CASE WHEN status = 'OCCUPIED' THEN 1 ELSE 0 END) AS occupied
            FROM parking_spaces
        """).fetchone()

        total_spaces = parking_counts["total_spaces"] or 0
        available_spaces = parking_counts["available"] or 0
        assigned_spaces = parking_counts["assigned"] or 0
        occupied_spaces = parking_counts["occupied"] or 0

        # Count active parking sessions
        current_vehicles = conn.execute("""
            SELECT COUNT(*)
            FROM parking_sessions
            WHERE status = 'ACTIVE'
        """).fetchone()[0]

        # Retrieve completed transactions
        transactions = pd.read_sql_query("""
            SELECT
                t.transaction_id AS 'Transaction ID',
                v.license_plate AS 'License Plate',
                p.space_number AS 'Parking Space',
                t.parking_duration AS 'Duration (Hours)',
                t.payment_amount AS 'Parking Fee',
                t.completed_at AS 'Completed At'
            FROM transactions t
            JOIN parking_sessions s
                ON t.session_id = s.session_id
            JOIN vehicles v
                ON s.vehicle_id = v.vehicle_id
            JOIN parking_spaces p
                ON s.space_id = p.space_id
            ORDER BY t.completed_at DESC
        """, conn)

    # Revenue calculations
    total_transactions = len(transactions)

    if not transactions.empty:
        total_revenue = transactions["Parking Fee"].sum()
    else:
        total_revenue = 0.0

    # Parking overview
    st.subheader("Parking Overview")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total Spaces", total_spaces)
    col2.metric("Available", available_spaces)
    col3.metric("Assigned", assigned_spaces)
    col4.metric("Occupied", occupied_spaces)
    col5.metric("Current Vehicles", current_vehicles)

    st.divider()

    # Revenue overview
    st.subheader("Revenue Overview")

    col1, col2 = st.columns(2)

    col1.metric("Completed Payments", total_transactions)

    col2.metric("Total Revenue", f"${total_revenue:.2f}")

    st.divider()

    # Parking capacity chart
    st.subheader("Parking Space Status")

    parking_data = pd.DataFrame({
        "Status": ["Available", "Assigned", "Occupied"],
        "Spaces": [
            available_spaces,
            assigned_spaces,
            occupied_spaces
        ]
    })

    st.bar_chart(
        parking_data,
        x="Status",
        y="Spaces"
    )

    st.divider()

    # Revenue chart
    st.subheader("Revenue Report")

    if not transactions.empty:

        st.bar_chart(
            transactions,
            x="License Plate",
            y="Parking Fee"
        )

    else:
        st.info("No payment information available yet.")

    st.divider()

    # Transaction history
    st.subheader("Completed Transactions")

    if not transactions.empty:

        display_transactions = transactions.copy()

        display_transactions["Parking Fee"] = (
            display_transactions["Parking Fee"].apply(
                lambda amount: f"${amount:.2f}"
            )
        )

        st.dataframe(
            display_transactions,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No completed transactions available.")

    st.caption("Smart Park Management System")
