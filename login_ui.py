import streamlit as st

from auth import (
    create_user,
    user_exists,
    verify_login,
    send_signup_otp
)

# ==========================================
# SESSION STATES
# ==========================================

if "otp" not in st.session_state:
    st.session_state.otp = None

if "otp_verified" not in st.session_state:
    st.session_state.otp_verified = False

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None


# ==========================================
# LOGIN / SIGNUP PAGE
# ==========================================

def login_signup_ui():

    st.markdown("""
    <h1 style='text-align:center;color:white;'>
    📦 FedEx AI Assistant
    </h1>
    """, unsafe_allow_html=True)

    menu = st.radio(
        "",
        ["Login", "Sign Up"],
        horizontal=True
    )

    # ======================================
    # SIGN UP
    # ======================================

    if menu == "Sign Up":

        st.subheader("Create Account")

        username = st.text_input("Username")

        email = st.text_input("Email")

        phone = st.text_input("Phone Number")

        password = st.text_input(
            "Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        # ==================================
        # SEND OTP
        # ==================================

        if st.button("Send OTP"):

            if (
                username and
                email and
                phone and
                password and
                confirm_password
            ):

                if password != confirm_password:

                    st.error("Passwords do not match")

                else:

                    existing_user = user_exists(phone)

                    if existing_user:

                        st.error(
                            "Phone number already registered"
                        )

                    else:

                        otp = send_signup_otp(email)

                        st.session_state.otp = otp

                        st.success(
                            f"OTP sent to {email}"
                        )

            else:

                st.warning(
                    "Please fill all fields"
                )

        # ==================================
        # VERIFY OTP
        # ==================================

        entered_otp = st.text_input(
            "Enter OTP"
        )

        if st.button("Verify OTP"):

            if entered_otp == st.session_state.otp:

                st.session_state.otp_verified = True

                st.success(
                    "OTP Verified Successfully"
                )

            else:

                st.error("Invalid OTP")

        # ==================================
        # CREATE ACCOUNT
        # ==================================

        if st.button("Create Account"):

            if st.session_state.otp_verified:

                create_user(
                    username,
                    phone,
                    password
                )

                st.success(
                    "Account Created Successfully"
                )

            else:

                st.warning(
                    "Please verify OTP first"
                )

    # ======================================
    # LOGIN
    # ======================================

    else:

        st.subheader("Login")

        phone = st.text_input(
            "Phone Number"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            valid_user = verify_login(
                phone,
                password
            )

            if valid_user:

                st.session_state.logged_in = True

                st.session_state.current_user = phone

                st.success("Login Successful")

                st.rerun()

            else:

                st.error(
                    "Invalid phone number or password"
                )