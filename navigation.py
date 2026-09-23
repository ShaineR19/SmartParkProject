import streamlit as st

def navigation():
    pages ={
        "Home": "app.py",
        "Parking": "parking.py",
        "Map": "map.py",
        "Vehicles": "vehicles.py",
        "Reservations": "reservations.py",
        "Payments": "payments.py",
        "Reports": "reports.py",
        "Login": "login.py"
    }
    selected_page = st.sidebar.radio(
        "Navigation",
        list(pages.keys())
    )

    return selected_page 
    