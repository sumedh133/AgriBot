import time
import streamlit as st
from bson import ObjectId

from app.agent.agent import get_agent
from app.agent.title_generation import generate_chat_title

from app.utils.chat_history import build_chat_history

from app.database.chat_repository import (
    create_conversation,
    add_message,
    get_messages,
    get_user_conversations,
    update_conversation_title
)
from app.database.profile_repository import ProfileRepository
from app.models.profile_model import FarmerProfile
from app.translation.translator import Translator
from app.memory.conversation_memory import ConversationMemory


def show_chat_page(cookies):

    # ---------------- STYLES ----------------
    st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        height: 42px;
        padding: 0 10px;
    }

    .stButton > button div,
    .stButton > button p {
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
        margin: 0;
    }

    button[kind="secondary"] {
        padding: 0 10px !important;
    }
    
    .profile-block {
        display: flex;
        flex-direction: column;
        gap: 2px;
    }

    .profile-label {
        font-size: 12px;
        opacity: 0.7;
    }

    .profile-email {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 100%;
        font-size: 14px;
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
            st.markdown(
                f"""
                <div class="profile-block">
                    <div class="profile-label">Profile</div>
                    <div class="profile-email" title="{st.session_state.user['email']}">
                        {st.session_state.user['email']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

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

        # ---------------- PROFILE FORM ----------------
        with st.expander("📝 Edit Farmer Profile", expanded=False):
            
            profile_repo = ProfileRepository()
            user_id = str(st.session_state.user["_id"])
            current_profile = profile_repo.get_profile(user_id)

            if not current_profile:
                current_profile = FarmerProfile(user_id=user_id)

            # Use simple inputs instead of st.form to avoid "scrambled" overlay
            new_location = st.text_input("Location", value=current_profile.location)
            
            soil_options = ["General", "Alluvial", "Black Soil", "Red Soil", "Laterite", "Sandy", "Clayey"]
            
            # Map old "Black (Regur)" if it exists
            current_soil = current_profile.soil_type
            if current_soil == "Black (Regur)": current_soil = "Black Soil"

            new_soil = st.selectbox(
                "Soil Type", 
                soil_options,
                index=soil_options.index(current_soil) if current_soil in soil_options else 0
            )

            new_irrigation = st.selectbox(
                "Irrigation",
                ["Rain-fed", "Canal", "Tube Well", "Drip", "Sprinkler"],
                index=["Rain-fed", "Canal", "Tube Well", "Drip", "Sprinkler"].index(current_profile.irrigation_type) if current_profile.irrigation_type in ["Rain-fed", "Canal", "Tube Well", "Drip", "Sprinkler"] else 0
            )
            
            crops_str = st.text_input("Crops (comma separated)", value=", ".join(current_profile.primary_crops))
            
            if st.button("Save Profile"):
                updated_profile = FarmerProfile(
                    user_id=user_id,
                    location=new_location,
                    soil_type=new_soil,
                    irrigation_type=new_irrigation,
                    primary_crops=[c.strip() for c in crops_str.split(",") if c.strip()]
                )
                profile_repo.save_profile(updated_profile)
                st.success("Profile updated!")
                time.sleep(0.5)
                st.rerun()

        st.divider()

        # ---------------- LANGUAGE SELECTOR ----------------
        st.subheader("🌐 Response Language")
        selected_lang = st.selectbox(
            "Select Language",
            ["English", "Hindi", "Marathi", "Telugu", "Tamil", "Gujarati", "Bengali", "Kannada"],
            index=0
        )

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
    profile_repo = ProfileRepository()
    user_profile = profile_repo.get_profile(str(st.session_state.user["_id"]))
    memory = ConversationMemory()
    user_memories = memory.get_memories(str(st.session_state.user["_id"]))
    llm = get_agent(profile=user_profile, memories=user_memories)

    # ---------------- EMPTY STATE ----------------
    if st.session_state.conversation_id is None:
        st.info("Start a new conversation by asking a question.")

    # ---------------- LOAD & DISPLAY HISTORY ----------------
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

        # -------- ASSISTANT RESPONSE --------
        with st.chat_message("assistant"):
            with st.spinner("Thinking... 🌱"):

                # ✅ ALWAYS FETCH LATEST HISTORY
                history = get_messages(conversation_id)

                # ✅ BUILD CONTEXT (LAST N MESSAGES)
                chat_history = build_chat_history(history)

                # ---------------- TRANSLATION (INPUT) ----------------
                translator = Translator()
                with st.spinner("Translating query..."):
                    english_input = translator.detect_and_translate_to_english(user_input)
                
                # ---------------- SAVE MEMORY ----------------
                memory.extract_and_save_facts(str(st.session_state.user["_id"]), user_input)

                # ✅ ADD CURRENT USER INPUT (Translated to English for AI)
                chat_history.append(("user", english_input))

                # ✅ CALL AGENT
                print(f"Chat History (English): {chat_history}")
                result = llm.invoke({"messages": chat_history})

                # ---------------- TRANSLATION (OUTPUT) ----------------
                raw_content = result["messages"][-1].content

                if isinstance(raw_content, list):
                    assistant_reply_en = "\n".join([
                        block["text"]
                        for block in raw_content
                        if isinstance(block, dict) and "text" in block
                    ])
                else:
                    assistant_reply_en = raw_content

                if selected_lang != "English":
                    with st.spinner(f"Translating to {selected_lang}... 🌱"):
                        assistant_reply = translator.translate(assistant_reply_en, selected_lang)
                else:
                    assistant_reply = assistant_reply_en

                st.write(assistant_reply)

        # -------- SAVE USER MESSAGE --------
        add_message(conversation_id, "user", user_input)

        # -------- SAVE ASSISTANT MESSAGE --------
        add_message(conversation_id, "assistant", assistant_reply)

        # -------- TITLE GENERATION --------
        if is_new_conversation:
            title = generate_chat_title(user_input)
            update_conversation_title(conversation_id, title)

        # -------- RERUN --------
        st.rerun()