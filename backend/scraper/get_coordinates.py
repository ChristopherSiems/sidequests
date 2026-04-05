import math
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

geolocator = Nominatim(user_agent="sidequests")

CAMPUS_LOCATIONS = {
    "uc ": (42.2510, -71.8232, "Higgins University Center, Clark University, Worcester, MA"),
    " uc ": (42.2510, -71.8232, "Higgins University Center, Clark University, Worcester, MA"),
    "university center": (42.2510, -71.8232, "Higgins University Center, Clark University, Worcester, MA"),
    "cusc": (42.2510, -71.8232, "Higgins University Center, Clark University, Worcester, MA"),
    "cmacd": (42.2510, -71.8232, "7 Hawthorne Street, Worcester, MA"),
    "macd": (42.2510, -71.8232, "7 Hawthorne Street, Worcester, MA"),   # catches "MACD 002" etc.
    "tilton": (42.2510, -71.8232, "Higgins University Center, Clark University, Worcester, MA"),
    "bickman": (42.2510, -71.8232, "57 Downing St, Worcester, MA"),
    "grind": (42.2510, -71.8232, "Higgins University Center, Clark University, Worcester, MA"),
    "rosenblatt": (42.2510, -71.8232, "Higgins University Center, Clark University, Worcester, MA"),
    "green": (42.2510, -71.8232, "950 Main Street, Worcester, MA"),
    "persky": (42.2510, -71.8232, "Higgins University Center, Clark University, Worcester, MA"),
    "lurie": (42.2510, -71.8232, "Higgins University Center, Clark University, Worcester, MA"),
    "blue room": (42.2510, -71.8232, "950 Main Street, Worcester, MA"),
    "jefferson": (42.2507, -71.8238, "950 Main Street, Worcester, MA"),
    "kneller": (42.2518, -71.8252, "Kneller Athletic Center, Clark University"),
    "dolan": (42.2530, -71.8200, "Dolan Field House, Clark University"),
    "dana": (42.2513, -71.8219, "Dana Commons, Clark University"),
    "craft studio": (42.2517, -71.8242, "Higgins University Center, Clark University, Worcester, MA"),
    "jonas": (42.2511, -71.8241, "Jonas Clark Hall, Clark University"),
    "jc": (42.2511, -71.8241, "Jonas Clark Hall, Clark University"),
    "corner house": (42.2492, -71.8247, "Corner House, 918 Main St, Worcester, MA"),
    "asher": (42.2502, -71.8255, "Higgins University Center, Clark University, Worcester, MA"),
    "center for counseling and personal growth": (42.2532, -71.8225, "114 Woodland St, Worcester, MA"),
    "academic commons": (42.2515, -71.8235, "Goddard Library, Clark University"),
    "goddard": (42.2515, -71.8235, "Goddard Library, Clark University"),
    "asec": (42.2504, -71.8222, "Alumni and Student Engagement Center, Clark University"),
    "ssj": (42.2504, -71.8222, "Alumni and Student Engagement Center, Clark University"),
    "little center": (42.2517, -71.8242, "950 Main St, Worcester, MA"),
    "bullock": (42.2522, -71.8240, "950 Main St, Worcester, MA"),
    "atwood": (42.2505, -71.8239, "950 Main Street, Worcester, MA"),
    "grace": (42.2510, -71.8245, "Higgins University Center, Clark University, Worcester, MA"),
    "carlson": (42.2511, -71.8255, "Carlson Hall, Clark University"),
    "bio life sciences": (42.2514, -71.8256, "13 Maywood St, Worcester, MA"),
    "higgins": (42.2513, -71.8250, "Higgins University Center, Clark University, Worcester, MA"),
    "dodd": (42.2525, -71.8235, "56 Downing St, Worcester, MA"),
    "hughes": (42.2526, -71.8238, "Hughes Hall, Clark University"),
    "red square": (42.2512, -71.8230, "Robert Goddard Memorial, Worcester, MA"),
    "the quad": (42.2512, -71.8234, "Robert Goddard Memorial, Worcester, MA"),
    "online": (42.2510, -71.8232, "Virtual / Online Event"),
}

def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return R * 2 * math.asin(math.sqrt(a))


CLARK_LAT, CLARK_LON = 42.2510, -71.8232
MAX_KM = 10
_last_geocode_time = 0.0  # module-level throttle tracker

def get_coordinates(address: str):
    global _last_geocode_time
    address_lower = address.lower()

    # 1. Match shorthand first (no network needed)
    for key, data in CAMPUS_LOCATIONS.items():
        if key in address_lower:
            return data

    # 2. Fallback to geocoder with rate limiting + retry
    elapsed = time.time() - _last_geocode_time
    if elapsed < 1.1:
        time.sleep(1.1 - elapsed)  # enforce ~1 req/sec

    for attempt in range(3):
        try:
            _last_geocode_time = time.time()
            query = address if "worcester" in address.lower() else f"{address}, Worcester, MA"
            print(f"  [Geocode] Looking up: '{address}'")
            location = geolocator.geocode(query, timeout=10)

            if location:
                km = _haversine_km(CLARK_LAT, CLARK_LON, location.latitude, location.longitude)
                if km <= MAX_KM:
                    return (location.latitude, location.longitude, f"{address}, Worcester, MA")
                else:
                    print(f"  [Skip] '{address}' is too far ({km:.1f}km).")
                    return None
            else:
                print(f"  [Skip] Could not geocode '{address}'.")
                return None

        except GeocoderTimedOut:
            wait = 2 ** attempt  # exponential backoff: 1s, 2s, 4s
            print(f"  [Timeout] '{address}' attempt {attempt+1}, retrying in {wait}s...")
            time.sleep(wait)
        except GeocoderServiceError as e:
            if "429" in str(e):
                wait = 5 * (attempt + 1)  # back off harder on rate limit
                print(f"  [RateLimit] Waiting {wait}s before retry...")
                time.sleep(wait)
            else:
                print(f"  [Error] Geocoding failed for '{address}': {e}")
                return None
        except Exception as e:
            print(f"  [Error] Geocoding failed for '{address}': {e}")
            return None

    print(f"  [Fail] Gave up geocoding '{address}' after 3 attempts.")
    return None