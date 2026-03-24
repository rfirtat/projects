import requests

BASE_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather(coords):
    latitude, longitude = coords
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    data = response.json()
    weather = data["current_weather"]

    return {
        "temperature": weather["temperature"],
        "windspeed": weather["windspeed"],
        "weathercode": weather["weathercode"]
    }