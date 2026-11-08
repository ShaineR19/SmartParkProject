
import streamlit as st
import hashlib
import secrets
import hmac

from backend.database import DatabaseManager


# Password hashing
def hash_password(password, salt):

    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        600000
    ).hex()


def show_login():

    # Connect to SQLite
    db = DatabaseManager()
    db.initialize_database()

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    st.title("Smart Park Login")
    st.write("Log in or create an account to access Smart Park.")
    st.divider()

    login_tab, signup_tab = st.tabs(
        ["Login", "Create Account"]
    )

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

            username = username.strip().lower()

            if not username or not password:
                st.error("Please enter your username and password.")

            else:

                with db.connect() as conn:

                    user = conn.execute(
                        """
                        SELECT * FROM users
                        WHERE username = ?
                        """,
                        (username,)
                    ).fetchone()

                if user:

                    entered_hash = hash_password(
                        password,
                        user["password_salt"]
                    )

                    if hmac.compare_digest(
                        entered_hash,
                        user["password_hash"]
                    ):

                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.full_name = user["full_name"]

                        # Open Dashboard after login
                        st.session_state["main_navigation"] = "Home"

                        st.success("Login successful!")
                        st.rerun()

                    else:
                        st.error("Incorrect password.")

                else:
                    st.error(
                        "Account not found. Please create an account."
                    )

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

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            new_username = new_username.strip().lower()

            if not name.strip() or not new_username:
                st.error("Please complete all fields.")

            elif len(new_password) < 8:
                st.error("Password must contain at least 8 characters.")

            elif new_password != confirm_password:
                st.error("Passwords do not match.")

            else:

                # Generate a unique password salt
                salt = secrets.token_hex(16)

                password_hash = hash_password(
                    new_password,
                    salt
                )

                try:

                    with db.connect() as conn:

                        conn.execute(
                            """
                            INSERT INTO users (
                                full_name,
                                username,
                                password_hash,
                                password_salt
                            )
                            VALUES (?, ?, ?, ?)
                            """,
                            (
                                name.strip(),
                                new_username,
                                password_hash,
                                salt
                            )
                        )

                        conn.commit()

                    st.success(
                        "Account created successfully! "
                        "You can now log in."
                    )

                except Exception as error:

                    if "UNIQUE constraint failed" in str(error):
                        st.error("Username already exists.")
                    else:
                        st.error("Unable to create account.")

    st.divider()
    st.caption("Smart Park Management System")
