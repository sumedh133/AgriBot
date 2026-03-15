import streamlit as st
from app.auth.jwt_handler import decode_token
from app.auth.auth_service import AuthService

auth_service = AuthService()


def show_auth_page(cookies):

    st.title("🌾 AgriAssist AI")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:

        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            
            if not email or not password:
                st.error("Email and password are required")
                return

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

    with tab2:

        email = st.text_input("Email", key="register_email")
        password = st.text_input("Password", type="password", key="register_password")

        if st.button("Register"):
            
            if not email or not password:
                st.error("Email and password are required")
                return

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