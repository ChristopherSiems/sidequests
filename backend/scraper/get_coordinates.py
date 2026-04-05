from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

geolocator = Nominatim(user_agent="sidequests")

def get_coordinates(address: str, default_lat: float = 42.2510, default_lon: float = -71.8232):
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        else:
            print(f"Could not geocode '{address}', defaulting to Clark")
            return default_lat, default_lon
    except GeocoderTimedOut:
        print(f"Geocoder timed out for '{address}', defaulting to Clark")
        return default_lat, default_lon
