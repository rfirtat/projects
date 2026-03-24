import requests


def get_coordinates(zipcode: str) -> tuple[float, float]:
    """
    Fetch latitude and longitude for a given ZIP code using the Zippopotam API.

    Parameters
    ----------
        zipcode (str): US ZIP code to look up.

    Returns
    -------
        tuple: (latitude, longitude) as floats.
    """

    # Assign response object and convert from JSON to python dict
    r = requests.get(f"https://api.zippopotam.us/us/{zipcode}", timeout=5)
    r.raise_for_status()
    response = r.json()

    # Parse through JSON to extract longitude and latitude as floats
    # By default only coordinates from first city in zipcode list are extracted
    latitude = float(response["places"][0]["latitude"])
    longitude = float(response["places"][0]["longitude"])

    return latitude, longitude



def main():
    response = get_coordinates(91756)

    print(type(response))
        
    print(response)


if __name__ == "__main__":
    main()