from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import GOOGLE_API_KEY

def generate_chat_title(user_message):
    
    # low temperature for more deterministic titles, can be adjusted as needed
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.2
    )

    prompt = f"""
        Generate a short title (maximum 6 words) for this conversation.

        User question:
        {user_message}

        Return ONLY the title.
    """

    response = llm.invoke(prompt)

    return response.content.strip()