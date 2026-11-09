import streamlit as st
import pandas as pd
from datetime import datetime
from backend.database import DatabaseManager
from backend.invoice_service import generate_parking_invoice_pdf


def show_invoices():
    st.title("Invoices")
    st.write("Generate and download PDF invoices for parked or completed vehicles.")
    st.divider()

    db = DatabaseManager()
    db.initialize_database()

    # Query vehicle sessions and completed transactions from SQLite
    with db.connect() as conn:
        records = pd.read_sql_query(
            """
            SELECT 
                t.transaction_id,
                v.license_plate,
                COALESCE(v.vehicle_name, '') AS vehicle_name,
                p.space_number,
                s.entry_time,
                COALESCE(s.exit_time, t.completed_at) AS exit_time,
                t.parking_duration,
                t.payment_amount,
                t.completed_at
            FROM transactions t
            JOIN parking_sessions s ON t.session_id = s.session_id
            JOIN vehicles v ON s.vehicle_id = v.vehicle_id
            JOIN parking_spaces p ON s.space_id = p.space_id
            ORDER BY t.transaction_id DESC
            """,
            conn,
        )

    if records.empty:
        st.info("No parking session records found in the database.")
        st.caption("Smart Park Management System")
        return

    # Dropdown selector for license plate & session
    records["display_label"] = records.apply(
        lambda r: f"{r['license_plate']} (Space: {r['space_number']} | Session #{int(r['transaction_id']) if pd.notnull(r['transaction_id']) else 'Active'})",
        axis=1,
    )

    selected_label = st.selectbox(
        "Select License Plate / Session",
        options=records["display_label"].tolist(),
    )

    selected_row = records[records["display_label"] == selected_label].iloc[0]

    # Session metric summary cards
    st.subheader("Session Details")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("License Plate", str(selected_row["license_plate"]))
    with c2:
        st.metric("Space Number", str(selected_row["space_number"]))
    with c3:
        dur = float(selected_row["parking_duration"])
        st.metric("Duration", f"{dur:.2f} hrs")
    with c4:
        amount = float(selected_row["payment_amount"])
        st.metric("Total Fee", f"${amount:.2f}")

    dur = float(selected_row["parking_duration"])
    total_fee = float(selected_row["payment_amount"])
    hourly_rate = round(total_fee / dur, 2) if dur > 0 else 5.00

    st.write("")

    # Generate and download PDF button
    if st.button("Generate Invoice PDF", use_container_width=True):
        try:
            tx_id = selected_row["transaction_id"]
            if pd.isna(tx_id) or not tx_id:
                tx_id = f"SES-{datetime.now().strftime('%Y%m%d%H%M')}"
            else:
                tx_id = int(tx_id)

            pdf_bytes = generate_parking_invoice_pdf(
                transaction_id=tx_id,
                license_plate=str(selected_row["license_plate"]),
                space_number=str(selected_row["space_number"]),
                entry_time=str(selected_row["entry_time"]),
                exit_time=str(selected_row["exit_time"]),
                duration_hours=dur,
                hourly_rate=hourly_rate,
                payment_amount=total_fee,
            )

            st.success("Invoice generated successfully!")
            st.download_button(
                label="Download Invoice PDF",
                data=pdf_bytes,
                file_name=f"Invoice_{selected_row['license_plate']}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"Error generating invoice: {e}")

    st.divider()
    st.caption("Smart Park Management System")