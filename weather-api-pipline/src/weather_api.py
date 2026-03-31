import requests

BASE_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather(latitude: float, longitude: float) -> dict:
    """
    Fetch current temperature, windspeed, weathercode for a given latitude/longitude 
    using the Open_Meteo API.

    Parameters
    ----------
        latitude : float
        longitude : float
            Coordinates to look up

    Returns
    -------
        dict 
        {
            "temperature": current temperature,
            "windspeed": current windspeed,
            "weathercode": current weathercode
        }
    """
    # Query parameters for API request
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True
    }

    # Assign response object and check for errors
    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise ValueError("Weather API request timed out")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Weather API error: {e}")

    # Convert JSON response to python dict for parsing
    # Open-Meteo nests current data under "current_weather"
    data = response.json()
    # Assign current_weather dict to variable, raise error if empty
    weather = data.get("current_weather")
    if not weather:
        raise ValueError("No weather data returned from API")
    # Extract values of interest from dict
    temperature = weather.get("temperature")
    windspeed = weather.get("windspeed")
    weathercode = weather.get("weathercode")
    # Check for incomplete data
    if temperature is None or windspeed is None or weathercode is None:
        raise ValueError("Incomplete weather data received")    
    # Return specific values of interest from weather dict
    return {
        "temperature": temperature,
        "windspeed": windspeed,
        "weathercode": weathercode
    }