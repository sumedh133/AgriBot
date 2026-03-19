import os
import requests
from langchain_core.tools import tool

@tool
def get_weather(location: str) -> str:
    """
    Fetches the current weather and the 5-day forecast for a given location.
    Always use this tool when a user asks about the weather (now or in the future), 
    or if it is safe to spray pesticides, water crops, or do field work.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Weather API key is missing."

    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": location,
        "appid": api_key,
        "units": "metric"
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Current weather (first item)
        current = data["list"][0]
        temp = current["main"]["temp"]
        description = current["weather"][0]["description"]
        humidity = current["main"]["humidity"]
        
        forecast_msg = f"Current weather in {location}: {temp}°C, {description}, Humidity: {humidity}%.\n"
        
        # Extract daily summary for next 3 days (approx 24h intervals)
        forecast_msg += "Forecast:\n"
        for i in range(8, 32, 8): # 8 * 3h = 24h intervals
            day_data = data["list"][i]
            date = day_data["dt_txt"].split(" ")[0]
            d_temp = day_data["main"]["temp"]
            d_desc = day_data["weather"][0]["description"]
            forecast_msg += f"- {date}: {d_temp}°C, {d_desc}\n"
            
        return forecast_msg
    except Exception as e:
        return f"Could not fetch weather data for {location}. Error: {str(e)}"