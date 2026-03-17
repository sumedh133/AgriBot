import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager 
from app.database.health_check import check_database_connection
from app.auth.jwt_handler import decode_token
from app.ui.auth_page import show_auth_page
from app.ui.chat_page import show_chat_page
from app.database.user_repository import UserRepository
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

st.set_page_config(page_title="AgriAssist AI")


cookies = EncryptedCookieManager(
    prefix="AgriBot",
    password="super_secret_cookie_key"
)

if not cookies.ready():
    st.stop()


# --------------------------------------------------
# Restore Session From Cookie (Auto Login)
# --------------------------------------------------

if "token" not in st.session_state and not st.session_state.get("logout", False):

    cookie_token = cookies.get("auth_token")

    # Only restore if cookie has a real token
    if cookie_token and cookie_token != "LOGGED_OUT":

        user_id = decode_token(cookie_token)

        if user_id:

            repo = UserRepository()
            user = repo.get_user_by_id(user_id)

            if user:
                st.session_state.token = cookie_token
                st.session_state.user = user


if "token" not in st.session_state:
    st.session_state.token = None


if not check_database_connection():
    st.error("Database connection failed")
    st.stop()


if st.session_state.token is None:
    show_auth_page(cookies)
else:
    show_chat_page(cookies)