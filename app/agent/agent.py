# from langchain_google_genai import ChatGoogleGenerativeAI
# from app.config import GOOGLE_API_KEY


# def get_agent():

#     llm = ChatGoogleGenerativeAI(
#         model="gemini-2.5-flash",
#         google_api_key=GOOGLE_API_KEY
#     )

#     return llm
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from app.config import GOOGLE_API_KEY
from app.agent.tools_registry import get_all_tools

def get_agent():
    """Initializes and returns the modern LangChain v1 agent."""
    
    # 1. Initialize the LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        temperature=0.2, 
        google_api_key=GOOGLE_API_KEY
    )

    # 2. Retrieve all registered tools
    tools = get_all_tools()

    # 3. Create the Agent (No AgentExecutor needed anymore!)
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="""You are AgriAssist AI, an expert agricultural assistant for farmers in India. 
        Provide clear, practical, and highly accurate farming advice.
        ALWAYS use your tools to fetch real-time weather or search the web for current data before answering factual questions.
        If a user asks about spraying pesticides, ALWAYS check the weather tool first."""
    )
    
    return agent