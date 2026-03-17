import time
import streamlit as st
from bson import ObjectId

from app.agent.agent import get_agent
from app.agent.title_generation import generate_chat_title

from app.database.chat_repository import (
    create_conversation,
    add_message,
    get_messages,
    get_user_conversations,
    update_conversation_title
)


def show_chat_page(cookies):

    # ---------------- STYLES ----------------
    st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        text-align: left;
        border-radius: 8px;
    }

    button[kind="secondary"][data-testid="baseButton-secondary"] {
        border: 2px solid #4CAF50 !important;
        background-color: rgba(76, 175, 80, 0.1) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------------- RESTORE STATE ----------------
    params = st.query_params

    if "conversation_id" not in st.session_state:
        if "chat" in params:
            st.session_state.conversation_id = ObjectId(params["chat"])
        else:
            st.session_state.conversation_id = None

    st.title("🌾 AgriAssist AI")

    # ---------------- SIDEBAR ----------------
    with st.sidebar:

        profile_col, logout_col = st.columns([5, 2])

        with profile_col:
            st.write(f"Profile: {st.session_state.user['email']}")

        with logout_col:
            if st.button("↩️", help="Logout"):
                cookies["auth_token"] = "LOGGED_OUT"
                cookies.save()
                time.sleep(0.3)

                st.query_params.clear()
                st.session_state.clear()
                st.session_state.logout = True
                st.rerun()

        st.divider()

        conversations = get_user_conversations(
            st.session_state.user["_id"]
        )

        title_col, button_col = st.columns([5, 2])

        with title_col:
            st.subheader(f"Your Chats ({len(conversations)})")

        with button_col:
            if st.button("➕", help="New Chat"):
                st.session_state.conversation_id = None
                st.query_params.clear()
                st.rerun()

        # -------- CHAT LIST --------
        for convo in conversations:

            title = convo.get("title", "New Chat")
            is_active = convo["_id"] == st.session_state.conversation_id

            if st.button(
                title,
                key=str(convo["_id"]),
                use_container_width=True,
                type="secondary" if is_active else "tertiary"
            ):
                st.session_state.conversation_id = convo["_id"]
                st.query_params["chat"] = str(convo["_id"])
                st.rerun()

    # ---------------- LLM ----------------
    llm = get_agent()

    # ---------------- EMPTY STATE ----------------
    if st.session_state.conversation_id is None:
        st.info("Start a new conversation by asking a question.")

    # ---------------- LOAD HISTORY ----------------
    if st.session_state.conversation_id:

        messages = get_messages(st.session_state.conversation_id)

        for msg in messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    # ---------------- INPUT ----------------
    user_input = st.chat_input("Ask your farming question")

    if user_input:

        is_new_conversation = False

        # -------- CREATE CONVO IF NEW --------
        if st.session_state.conversation_id is None:

            conversation_id = create_conversation(
                st.session_state.user["_id"]
            )

            st.session_state.conversation_id = conversation_id
            st.query_params["chat"] = str(conversation_id)

            is_new_conversation = True

        conversation_id = st.session_state.conversation_id

        # -------- SHOW USER MESSAGE --------
        with st.chat_message("user"):
            st.write(user_input)

        # -------- SAVE USER MESSAGE --------
        add_message(conversation_id, "user", user_input)

        # -------- ASSISTANT RESPONSE --------
        with st.chat_message("assistant"):
            with st.spinner("Thinking... 🌱"):

                result = llm.invoke({"messages": [("user", user_input)]})

                raw_content = result["messages"][-1].content

                if isinstance(raw_content, list):
                    assistant_reply = "\n".join([
                        block["text"]
                        for block in raw_content
                        if isinstance(block, dict) and "text" in block
                    ])
                else:
                    assistant_reply = raw_content

                st.write(assistant_reply)

        # -------- SAVE ASSISTANT --------
        add_message(conversation_id, "assistant", assistant_reply)

        # -------- TITLE GENERATION --------
        if is_new_conversation:
            title = generate_chat_title(user_input)
            update_conversation_title(conversation_id, title)

        # -------- RERUN FOR SIDEBAR UPDATE --------
        st.rerun()