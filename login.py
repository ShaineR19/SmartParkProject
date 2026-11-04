
import streamlit as st


def show_login():

    # Temporary account storage
    if "users" not in st.session_state:
        st.session_state.users = {}

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # Login page heading
    st.title("Smart Park Login")
    st.write("Log in or create an account to access Smart Park.")
    st.divider()

    # Login and Create Account tabs
    login_tab, signup_tab = st.tabs(["Login", "Create Account"])

    # LOGIN

    with login_tab:

        st.subheader("Welcome Back")

        username = st.text_input(
            "Username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login", use_container_width=True):

            if not username.strip() or not password:
                st.error("Please enter your username and password.")

            elif username in st.session_state.users:

                if st.session_state.users[username] == password:

                    st.session_state.logged_in = True
                    st.session_state.username = username

                    # Open Dashboard after login
                    st.session_state["main_navigation"] = "Home"

                    st.success("Login successful!")
                    st.rerun()

                else:
                    st.error("Incorrect password.")

            else:
                st.error("Account not found. Please create an account.")

    # CREATE ACCOUNT

    with signup_tab:

        st.subheader("Create a New Account")

        name = st.text_input(
            "Full Name",
            key="signup_name"
        )

        new_username = st.text_input(
            "Choose a Username",
            key="signup_username"
        )

        new_password = st.text_input(
            "Create Password",
            type="password",
            key="signup_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="confirm_password"
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

                st.success(
                    "Account created successfully! You can now log in."
                )

    st.divider()
    st.caption("Smart Park Management System")
