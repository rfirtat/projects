import requests

def get_coordinates(zipcode: str) -> tuple[str, float, float]:
    """
    Fetch city name, latitude, longitude for a given ZIP code using the Zippopotam API.

    Parameters
    ----------
        zipcode (str): US ZIP code to look up.

    Returns
    -------
        tuple: (city name, latitude, longitude).
    """

    # Assign response object and convert from JSON to python dict
    try:
        r = requests.get(f"https://api.zippopotam.us/us/{zipcode}", timeout=5)
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        raise ValueError(f"Invalid ZIP code: {zipcode}")
    except requests.exceptions.Timeout:
        raise ValueError("Request timed out")
    except requests.exceptions.RequestException:
        raise ValueError("Network error occurred")
    response = r.json()

    # Parse through JSON to extract longitude and latitude as floats
    # By default only coordinates from first city in zipcode list are extracted
    city = response["places"][0]["place name"]
    lat = float(response["places"][0]["latitude"])
    lon = float(response["places"][0]["longitude"])

    return city, lat, lon



def main():
    #city, lat, lon, response = get_coordinates(91765)
    #print(json.dumps(response, indent=4))
    pass


if __name__ == "__main__":
    main()