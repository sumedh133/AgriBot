import os
import requests
from langchain_core.tools import tool

@tool
def get_weather(location: str) -> str:
    """
    Fetches the current weather forecast for a given location.
    Always use this tool when a user asks about the weather, or if it is safe to spray pesticides, water crops, or do field work.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Weather API key is missing."

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": api_key,
        "units": "metric"
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        
        return f"The current weather in {location} is {temp}°C with {description}. Humidity is {humidity}%."
    except Exception as e:
        return f"Could not fetch weather data for {location}. Error: {str(e)}"