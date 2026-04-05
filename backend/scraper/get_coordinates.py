import math
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

geolocator = Nominatim(user_agent="sidequests")

CAMPUS_LOCATIONS = {
    "uc":           (42.2510, -71.8232),
    "university center": (42.2510, -71.8232),
    "cusc": (42.2510, -71.8232),
    "cmacd": (42.2510, -71.8232),
    "tilton": (42.2510, -71.8232),
    "bickman": (42.2510, -71.8232),
    "grind": (42.2510, -71.8232),
    "rosenblatt": (42.2510, -71.8232),
    "green": (42.2510, -71.8232),
    "persky": (42.2510, -71.8232),
    "jefferson": (42.2510, -71.8232),
    "kneller": (42.2510, -71.8232),
    "dolan": (42.2510, -71.8232),
    "dana": (42.2510, -71.8232),
    "craft studio": (42.2510, -71.8232),
    "jonas": (42.2510, -71.8232),
    "corner house": (42.2510, -71.8232),
    "asher": (42.2510, -71.8232),
    "center for counseling and personal growth": (42.2510, -71.8232),
    "academic commons": (42.2510, -71.8232),
    "asec": (42.2510, -71.8232),
    "little center": (42.2510, -71.8232),
    "bullock": (42.2510, -71.8232),
    "lurie": (42.2510, -71.8232),
    "atwood": (42.2510, -71.8232),
    "online": (42.2510, -71.8232),
    "grace": (42.2510, -71.8232),
    "carlson": (42.2510, -71.8232),
    "bio life sciences": (42.2510, -71.8232),
    "higgins": (42.2510, -71.8232),
    "ssj": (42.2510, -71.8232),
    "jc": (42.2510, -71.8232),
    "dodd": (42.2510, -71.8232),
    "hughes": (42.2510, -71.8232),
    "blue room": (42.2510, -71.8232),
    "goddard": (42.2510, -71.8232),
    "red square": (42.2510, -71.8232),
    "the quad": (42.2510, -71.8232),
}

# haversine formula: calculates straight line distance in km between two coordinate pairs in degrees
def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return R * 2 * math.asin(math.sqrt(a))

CLARK_LAT, CLARK_LON = 42.2510, -71.8232
MAX_KM = 10

# checks for 'shorthand' campus names first, returning center of campus coordinates if it is.
# next it runs a real address through coordinate conversion, throwing an error if it fails or if
# the resulting coordinates are greater than 10km away from Clark.
def get_coordinates(address: str):
    address_lower = address.lower().strip()
    for key, coords in CAMPUS_LOCATIONS.items():
        if key in address_lower:
            print(f"  '{address}' matched campus shorthand '{key}'")
            return coords

    try:
        location = geolocator.geocode(f"{address}, Worcester, MA", timeout=10)
        if location:
            km = _haversine_km(CLARK_LAT, CLARK_LON, location.latitude, location.longitude)
            if km <= MAX_KM:
                return location.latitude, location.longitude
            else:
                raise ValueError(f"'{address}' geocoded too far ({km:.1f}km from Clark)")
        else:
            raise ValueError(f"Could not geocode '{address}'")
    except GeocoderTimedOut:
        raise ValueError(f"Geocoder timed out for '{address}'")