import requests

def get_coordinates(zipcode: str) -> tuple[str, float, float]:
    """
    Fetch city name, latitude, longitude for a given ZIP code using the Zippopotam API.

    Parameters
    ----------
        zipcode (str): US ZIP code to look up.

    Returns
    -------
        tuple[str, float, float]: (city name, latitude, longitude).
    """

    # Assign response object and check for errors
    try:
        response = requests.get(f"https://api.zippopotam.us/us/{zipcode}", timeout=5)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        raise ValueError(f"Invalid ZIP code: {zipcode}")
    except requests.exceptions.Timeout:
        raise ValueError("Request timed out")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Network error occurred: {e}")
    
    # Convert JSON to python dict
    data = response.json()

    # Parse through JSON to extract longitude and latitude as floats and city name
    # Assign places list to variable, raise error if empty
    places = data.get("places")
    if not places:
        raise ValueError(f"No location found for ZIP code: {zipcode}")
    # By default only coordinates from first city in zipcode list are extracted
    place = places[0]
    # Extract information from place dictionary
    city = place.get("place name")
    lat = place.get("latitude")
    lon = place.get("longitude")
    # Check for incomplete data
    if city is None or lat is None or lon is None:
        raise ValueError("Incomplete data received from API")
    # Ensure correct typing of lat/lon
    lat = float(lat)
    lon = float(lon)

    return city, lat, lon
