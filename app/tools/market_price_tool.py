from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool

@tool
def get_market_prices(crop: str, mandi: str = "") -> str:
    """
    Fetches the latest mandi prices for a specific crop and location.
    Use this tool whenever a user asks for 'mandi prices', 'crop prices', or 'current rates'.
    """
    search = TavilySearchResults(max_results=3)
    query = f"current mandi price of {crop}"
    if mandi:
        query += f" in {mandi}"
    query += " today India"
    
    try:
        results = search.run(query)
        if not results:
            return f"No recent market price information found for {crop}."
        
        # Format the search results into a readable string for the LLM
        response = f"Latest market trends for {crop}:\n"
        for res in results:
            response += f"- [Source: {res['url']}]\n  {res['content'][:200]}...\n"
        
        return response
    except Exception as e:
        return f"Error fetching market prices: {str(e)}"
