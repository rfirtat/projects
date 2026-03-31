import requests

BASE_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather(latitude: float, longitude: float) -> dict:
    """
    Fetch current temperature, windspeed, weathercode for a given latitude/longitude 
    using the Open_Meteo API.

    Parameters
    ----------
        latitude, longitude: Coordinates to look up.

    Returns
    -------
        dict: {
            "temperature": current temperature,
            "windspeed": current windspeed,
            "weathercode": current weathercode
        }.
    """
    # Put lat/long into structured dict for use with .get method
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True
    }

    # Use .get() with URL and params to obtain response object
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    # Convert JSON response to python dict for parsing
    data = response.json()
    # Asign "current_weather" value (dict) to a variable
    weather = data["current_weather"]

    # Return specific values of interest from weather dict
    return {
        "temperature": weather["temperature"],
        "windspeed": weather["windspeed"],
        "weathercode": weather["weathercode"]
    }