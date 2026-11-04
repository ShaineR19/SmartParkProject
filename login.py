
import streamlit as st

def show_login():

    login_status(False)
    
    st.title("Smart Park Login")
    st.write("Log in or create an account to access Smart Park.")
    st.divider()

    # Temporary account storage
    if "users" not in st.session_state:
        st.session_state.users = {}

    login_tab, signup_tab = st.tabs(["Login", "Create Account"])

    # LOGIN
    with login_tab:

        st.subheader("Welcome Back")

        username = st.text_input("Username", key="login_username")
        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login", use_container_width=True):

            if username in st.session_state.users:
                if st.session_state.users[username] == password:

                    st.session_state.logged_in = login_status(True)
                    st.session_state.username = username

                    st.success("Login successful!")
                    

                else:
                    st.error("Incorrect password.")

            else:
                st.error("Account not found. Please create an account.")

    # CREATE ACCOUNT
    with signup_tab:

        st.subheader("Create a New Account")

        name = st.text_input("Full Name", key="signup_name")
        new_username = st.text_input("Choose a Username")
        new_password = st.text_input(
            "Create Password",
            type="password"
        )
        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        if st.button("Create Account", use_container_width=True):

            if not name.strip() or not new_username.strip():
                st.error("Please complete all fields.")

            elif not new_password:
                st.error("Please create a password.")

            elif new_password != confirm_password:
                st.error("Passwords do not match.")

            elif new_username in st.session_state.users:
                st.error("Username already exists.")

            else:
                st.session_state.users[new_username] = new_password

                st.success("Account created successfully! You can now log in.")

    # LOGOUT
    if st.session_state.get("logged_in", False):

        st.divider()
        st.success(f"Logged in as {st.session_state.username}")

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()

    st.caption("Smart Park Management System")

def login_status(bool):
    return bool