
import streamlit as st

from backend.payment_service import PaymentService
from navigation import navigation
from dashboard import show_dashboard
from parking import show_parking
from vehicles import show_vehicles
from payments import show_payments
from reports import show_reports
from login import show_login


# Page configuration
st.set_page_config(
    page_title="Smart Park",
    page_icon="🅿️",
    layout="wide"
)

# Shared design - Green Theme
st.markdown(
    """
    <style>

    /* Main background */
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"] {
        background-color: #EDF4EE !important;
    }

    /* Top header */
    [data-testid="stHeader"] {
        background-color: #EDF4EE !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div:first-child {
        background-color: #DCE9DF !important;
    }

    /* Sidebar text */
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {
        color: #294B3A !important;
    }

    /* Sidebar hover */
    [data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background-color: #C9DDCE !important;
    }

    /* Selected navigation */
    [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
        background-color: #B8D2BF !important;
    }

    /* Headings */
    h1, h2, h3 {
        color: #294B3A !important;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #D7E4D9;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    }

    /* Buttons */
    .stButton > button,
    .stFormSubmitButton > button {
        background-color: #52796F !important;
        color: white !important;
        border-radius: 8px;
        border: none;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        background-color: #294B3A !important;
        color: white !important;
    }

    /* Input fields */
    .stTextInput input,
    .stNumberInput input {
        border-radius: 8px;
    }

    /* Data tables */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        border: 1px solid #D7E4D9;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Navigation
page = "login"
logged_in = login_status()

# Display selected page
if not st.session_state.get("logged_in", False):
    show_login()

else:
    page = navigation()

    if page == "Home":
        show_dashboard()
    
    elif page == "Parking":
        show_parking()
        
    elif page == "Parking":
        show_parking()

    elif page == "Map":
        st.title("Parking Lot Map")

        map_data = {
                "lat": [34.6805],
                "lon": [-79.1950]
            }

        st.map(map_data)

    elif page == "Vehicles":
        show_vehicles()

    elif page == "Payments":
        show_payments()

    elif page == "Reports":
        show_reports()

