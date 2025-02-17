import webbrowser
import requests
from config import OPENCAGE_API_KEY, OPENCAGE_API_URL

def get_location_details(location):
    """Get detailed information about a location using OpenCage Geocoding API."""
    try:
        response = requests.get(
            OPENCAGE_API_URL,
            params={"q": location, "key": OPENCAGE_API_KEY, "limit": 1}
        )
        response.raise_for_status()
        data = response.json()

        if data["results"]:
            result = data["results"][0]
            formatted_address = result["formatted"]
            coordinates = result["geometry"]
            return {
                "address": formatted_address,
                "lat": coordinates["lat"],
                "lng": coordinates["lng"],
                "success": True
            }
        else:
            return {"success": False, "error": "Location not found"}
            
    except Exception as e:
        print(f"OpenCage API error: {e}")
        return {"success": False, "error": str(e)}

def open_in_maps(location):
    """
    Open the specified location in Google Maps and return a status message.
    Returns formatted address if successful, error message if not.
    """
    try:
        # First get location details
        location_data = get_location_details(location)
        
        if location_data["success"]:
            # Format the coordinates for Google Maps
            lat, lng = location_data["lat"], location_data["lng"]
            maps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lng}"
            webbrowser.open(maps_url)
            return location_data["address"]
        else:
            return None

    except Exception as e:
        print(f"Error opening maps: {e}")
        return None

def get_directions(origin, destination):
    """Get directions between two locations using Google Maps."""
    try:
        # Format the locations for URL
        origin_formatted = origin.replace(' ', '+')
        destination_formatted = destination.replace(' ', '+')
        directions_url = f"https://www.google.com/maps/dir/?api=1&origin={origin_formatted}&destination={destination_formatted}"
        webbrowser.open(directions_url)
        return True
    except Exception as e:
        print(f"Error getting directions: {e}")
        return False