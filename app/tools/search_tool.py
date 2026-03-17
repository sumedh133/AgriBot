import os
from langchain_community.tools.tavily_search import TavilySearchResults

def get_search_tool():
    """
    Returns the Tavily Search tool for general agricultural queries, news, and market trends.
    """
    # LangChain already has a pre-built tool for Tavily!
    return TavilySearchResults(max_results=3)