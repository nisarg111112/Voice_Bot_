import requests
from config import OPEN_METEO_URL, OPENCAGE_API_KEY, OPENCAGE_API_URL
from datetime import datetime

def get_coordinates(city):
    """Fetch latitude and longitude for a city using OpenCage Geocoder API."""
    try:
        response = requests.get(
            OPENCAGE_API_URL,
            params={"q": city, "key": OPENCAGE_API_KEY, "limit": 1}
        )
        response.raise_for_status()
        data = response.json()

        if data["results"]:
            location = data["results"][0]["geometry"]
            return location["lat"], location["lng"]
        else:
            print(f"No results found for city: {city}")
            return None, None
    except Exception as e:
        print(f"OpenCage API error: {e}")
        return None, None

def fetch_weather(city):
    """Fetch current weather data for a city."""
    latitude, longitude = get_coordinates(city)
    if latitude is not None and longitude is not None:
        try:
            # First, get current weather only
            current_params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation_probability,pressure_msl,wind_speed_10m,weather_code"
            }
            
            response = requests.get(OPEN_METEO_URL, params=current_params)
            response.raise_for_status()
            weather_data = response.json()
            
            if "current" in weather_data:
                current = weather_data["current"]
                
                # Weather codes dictionary
                weather_descriptions = {
                    0: "clear sky",
                    1: "mainly clear",
                    2: "partly cloudy",
                    3: "overcast",
                    45: "foggy",
                    48: "depositing rime fog",
                    51: "light drizzle",
                    53: "moderate drizzle",
                    55: "dense drizzle",
                    61: "slight rain",
                    63: "moderate rain",
                    65: "heavy rain",
                    71: "slight snow fall",
                    73: "moderate snow fall",
                    75: "heavy snow fall",
                    95: "thunderstorm"
                }
                
                weather_condition = weather_descriptions.get(current["weather_code"], "unknown condition")
                
                # Format for TTS
                return (f"{city}. "
                       f"Temperature {int(current['temperature_2m'])} degrees. "
                       f"Feels like {int(current['apparent_temperature'])} degrees. "
                       f"{weather_condition}. "
                       f"Wind speed {int(current['wind_speed_10m'])} kilometers per hour. "
                       f"Humidity {int(current['relative_humidity_2m'])} percent. "
                       f"Air pressure {int(current['pressure_msl'])} hectopascals.")
            else:
                return f"Weather data unavailable for {city}"
        except Exception as e:
            print(f"Weather API error: {e}")
            return "Weather data currently unavailable"
    else:
        return f"Location not found {city}"
