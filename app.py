import streamlit as st

from navigation import navigation
from dashboard import show_dashboard
from parking import show_parking
from vehicles import show_vehicles
from payments import show_payments
from reports import show_reports
from login import show_login
#from invoices import show_invoices
from backend.database import DatabaseManager


# Page configuration
st.set_page_config(
    page_title="Smart Park",
    page_icon="🅿️",
    layout="wide"
)
# Initialize database
db = DatabaseManager()
db.initialize_database()

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

# Check whether the user is logged in
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Show Login page first
if not st.session_state.logged_in:

    show_login()

# Show the rest of the application after login
else:

    page = navigation()

    # Logged-in user information and Logout button
    with st.sidebar:
        st.divider()

        st.caption(
            f"Logged in as: {st.session_state.get('username', '')}"
        )

        if st.button("Logout", use_container_width=True):

            st.session_state.logged_in = False
            st.session_state.username = ""

            st.rerun()

    # Application pages
    if page == "Home":
        show_dashboard()

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

    elif page == "Invoices":  
        show_invoices()