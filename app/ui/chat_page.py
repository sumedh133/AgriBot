import streamlit as st
from app.agent.agent import get_agent

def show_chat_page(cookies):

    st.title("🌾 AgriAssist AI")

    # Sidebar
    with st.sidebar:
        st.write(f"👤 Logged in as: {st.session_state.user['email']}")

        if st.button("Logout"):
            cookies["auth_token"] = ""
            cookies.save()
            st.session_state.clear()
            st.session_state.logout = True
            st.rerun()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    llm = get_agent()

    # 1. ALWAYS DRAW HISTORY FIRST
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"]) 

    user_input = st.chat_input("Ask your farming question")

    if user_input:
        # 2. Add user message to state and draw their chat bubble
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # 3. Draw the assistant's bubble with a loading spinner
        with st.chat_message("assistant"):
            with st.spinner("Fetching real-time data..."):
                
                # Package the input and call the agent
                inputs = {"messages": [("user", user_input)]}
                result = llm.invoke(inputs)
                
                # Get the raw content from the last message
                raw_content = result["messages"][-1].content
                
                # Gemini sometimes returns a list of blocks instead of a plain string
                if isinstance(raw_content, list):
                    # Extract only the "text" from those blocks
                    final_answer = "\n".join([block["text"] for block in raw_content if isinstance(block, dict) and "text" in block])
                else:
                    # If it is already a normal string, just use it directly
                    final_answer = raw_content

                st.write(final_answer)

        # 4. Save the agent's correct response to the state
        st.session_state.messages.append(
            {"role": "assistant", "content": final_answer}
        )