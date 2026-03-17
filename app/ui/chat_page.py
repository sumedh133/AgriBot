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

    st.markdown("""
<style>

/* Default chat button */
.stButton > button {
    width: 100%;
    text-align: left;
    border-radius: 8px;
}

/* Active chat highlight */
button[kind="secondary"][data-testid="baseButton-secondary"] {
    border: 2px solid #4CAF50 !important;
    background-color: rgba(76, 175, 80, 0.1) !important;
}

</style>
""", unsafe_allow_html=True)
    
    # Restore conversation from URL
    params = st.query_params

    if "conversation_id" not in st.session_state:

        if "chat" in params:
            st.session_state.conversation_id = ObjectId(params["chat"])
        else:
            st.session_state.conversation_id = None

    st.title("🌾 AgriAssist AI")

    # Sidebar
    with st.sidebar:

        profile_col, logout_col = st.columns([5,2], vertical_alignment="center")

        with profile_col:
            st.write(f"Profile: {st.session_state.user['email']}")

        with logout_col:
            if st.button("↩️", help="Logout"):
                cookies["auth_token"] = "LOGGED_OUT"
                cookies.save()
                time.sleep(0.5)
                st.query_params.clear()

                st.session_state.clear()
                st.session_state.logout = True
                st.rerun()

        st.divider()

        conversations = get_user_conversations(
            st.session_state.user["_id"]
        )

        title_col, button_col = st.columns([5,2])

        with title_col:
            st.subheader(f"Your Chats ({len(conversations)})")

        with button_col:
            if st.button("➕", help="New Chat"):
                if st.session_state.conversation_id is not None:
                    st.session_state.conversation_id = None
                    st.query_params.clear()

        # Chat List
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

    llm = get_agent()

    # Empty chat state
    if st.session_state.conversation_id is None:
        st.info("Start a new conversation by asking a question.")

    # Load messages
    if st.session_state.conversation_id:

        messages = get_messages(st.session_state.conversation_id)

        for msg in messages:

            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    # Chat input
    user_input = st.chat_input("Ask your farming question")

    if user_input:

        is_new_conversation = False

        # Create conversation on first message
        if st.session_state.conversation_id is None:

            conversation_id = create_conversation(
                st.session_state.user["_id"]
            )

            st.session_state.conversation_id = conversation_id
            st.query_params["chat"] = str(conversation_id)

            is_new_conversation = True

        conversation_id = st.session_state.conversation_id

        # Save user message
        add_message(
            conversation_id,
            "user",
            user_input
        )

        # Show user message immediately
        with st.chat_message("user"):
            st.write(user_input)

        # LLM response
        response = llm.invoke(user_input)
        assistant_reply = response.content

        # Save assistant message
        add_message(
            conversation_id,
            "assistant",
            assistant_reply
        )

        # Show assistant message
        with st.chat_message("assistant"):
            st.write(assistant_reply)

        # Generate chat title only once
        if is_new_conversation:

            title = generate_chat_title(user_input)

            update_conversation_title(
                conversation_id,
                title
            )

        # Force rerun so sidebar updates
        st.rerun()