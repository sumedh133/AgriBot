import streamlit as st
import re

from app.auth.jwt_handler import decode_token
from app.auth.auth_service import AuthService

auth_service = AuthService()


def is_valid_email(email: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


def show_auth_page(cookies):

    # ===== CSS FIXES =====
    st.markdown("""
    <style>

    /* Hide "Press Enter to submit" text */
    [data-testid="stForm"] div small,
    [data-testid="stForm"] small,
    [data-testid="InputInstructions"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* Remove extra spacing caused by that hint */
    [data-testid="stForm"] div:has(small) {
        margin-bottom: 0px !important;
    }

    /* Optional: cleaner form look */
    [data-testid="stForm"] {
        border: none;
    }

    </style>
    """, unsafe_allow_html=True)

    st.title("🌾 AgriAssist AI")

    tab1, tab2 = st.tabs(["Login", "Register"])

    # ===================== LOGIN =====================
    with tab1:

        with st.form("login_form"):

            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")

            submitted = st.form_submit_button("Login", use_container_width=True)

            if submitted:

                error_msg = None

                if not email:
                    error_msg = "Please enter your email"
                elif not is_valid_email(email):
                    error_msg = "Please enter a valid email"
                elif not password:
                    error_msg = "Password cannot be empty"

                if error_msg:
                    st.warning(error_msg)
                else:
                    with st.spinner("Logging in..."):
                        token, user, error = auth_service.login(email, password)

                    if error:
                        st.error(error)
                    else:
                        st.session_state.token = token
                        st.session_state.user_id = decode_token(token)
                        st.session_state.user = user

                        cookies["auth_token"] = token
                        cookies.save()

                        st.rerun()

    # ===================== REGISTER =====================
    with tab2:

        with st.form("register_form"):

            email = st.text_input("Email", key="register_email")
            password = st.text_input("Password", type="password", key="register_password")

            submitted = st.form_submit_button("Register", use_container_width=True)

            if submitted:

                error_msg = None

                if not email:
                    error_msg = "Please enter your email"
                elif not is_valid_email(email):
                    error_msg = "Please enter a valid email"
                elif not password:
                    error_msg = "Password cannot be empty"

                if error_msg:
                    st.warning(error_msg)
                else:
                    with st.spinner("Creating account..."):
                        token, user, error = auth_service.register(email, password)

                    if error:
                        st.error(error)
                    else:
                        st.session_state.token = token
                        st.session_state.user_id = decode_token(token)
                        st.session_state.user = user

                        cookies["auth_token"] = token
                        cookies.save()

                        st.rerun()