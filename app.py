import streamlit as st

from navigation import navigation

st.set_page_config(
    page_title="Smart Park " ,
    page_icon="🅿️" ,
    layout="wide"

)

page = navigation()

st.title("Smart Park")

st.write("Welcome to the Smart Parking System")

if page == "Home" :
    st.subheader("Home")
    st.write("Welcome to your parking lot dashboard")

elif page == "Parking":
    st.subheader("Parking")
    st.write("View available and occupied parking spaces.")

elif page == "Map" :
    st.subheader("Parking Lot Map")

    map_data = {
        "lat": [34.6805],
        "lon": [-79.1950]
    }

    st.map(map_data)

elif page == "Vehicles" :
    st.subheader("Vehicles")
    st.write ("Manage vehicles in the parking lot.")

elif page == "Reservations" :
    st.subheader ("Reservations")
    st.write ("Manage parking reservations.")

elif page == "Payments" :
    st.subheader("Payments")
    st.write("Manage parking payments.")

elif page == "Reports" :
    st.subheader("Reports")
    st.write("View parking lot reports.")

elif page == "Login" :
    st.subheader ("Login")
    st.write("Login page coming soon.")

