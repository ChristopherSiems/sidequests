import math
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

geolocator = Nominatim(user_agent="sidequests")

# Expanded: Maps shorthand -> (Lat, Lon, Full Google-Friendly Name)
CAMPUS_LOCATIONS = {
    "uc": (42.2510, -71.8232, "Higgins University Center, Clark University"),
    "university center": (42.2510, -71.8232, "Higgins University Center, Clark University"),
    "cusc": (42.2510, -71.8232, "Higgins University Center, Clark University"),
    "cmacd": (42.2510, -71.8232, "Higgins University Center, Clark University"),
    "tilton": (42.2510, -71.8232, "Tilton Hall, Higgins University Center, Clark University"),
    "bickman": (42.2510, -71.8232, "Bickman Fitness Center, Clark University"),
    "grind": (42.2510, -71.8232, "The Grind, Higgins University Center, Clark University"),
    "rosenblatt": (42.2510, -71.8232, "Rosenblatt Conference Room, University Center"),
    "green": (42.2510, -71.8232, "Green Floor, Higgins University Center"),
    "persky": (42.2510, -71.8232, "Persky Conference Room, University Center"),
    "lurie": (42.2510, -71.8232, "Lurie Conference Room, University Center"),
    "blue room": (42.2510, -71.8232, "Blue Room, Higgins University Center"),
    
    "jefferson": (42.2507, -71.8238, "Jefferson Academic Center, Clark University"),
    "kneller": (42.2518, -71.8252, "Kneller Athletic Center, Clark University"),
    "dolan": (42.2530, -71.8200, "Dolan Field House, Clark University"),
    "dana": (42.2513, -71.8219, "Dana Commons, Clark University"),
    "craft studio": (42.2517, -71.8242, "Little Center Craft Studio, Clark University"),
    "jonas": (42.2511, -71.8241, "Jonas Clark Hall, Clark University"),
    "jc": (42.2511, -71.8241, "Jonas Clark Hall, Clark University"),
    "corner house": (42.2492, -71.8247, "Corner House, 918 Main St, Worcester, MA"),
    "asher": (42.2502, -71.8255, "Asher Student Center, Clark University"),
    "center for counseling and personal growth": (42.2532, -71.8225, "501 Park Ave, Worcester, MA"),
    
    "academic commons": (42.2515, -71.8235, "Academic Commons, Goddard Library, Clark University"),
    "goddard": (42.2515, -71.8235, "Goddard Library, Clark University"),
    "asec": (42.2504, -71.8222, "Alumni and Student Engagement Center, Clark University"),
    "ssj": (42.2504, -71.8222, "Alumni and Student Engagement Center, Clark University"),
    
    "little center": (42.2517, -71.8242, "Little Center, Clark University"),
    "bullock": (42.2522, -71.8240, "Bullock Hall, Clark University"),
    "atwood": (42.2505, -71.8239, "Atwood Hall, Clark University"),
    "grace": (42.2510, -71.8245, "Grace Conference Room, Clark University"),
    "carlson": (42.2511, -71.8255, "Carlson Hall, Clark University"),
    "bio life sciences": (42.2514, -71.8256, "Lasry Center for Bioscience, Clark University"),
    "higgins": (42.2513, -71.8250, "Higgins Labs, Clark University"),
    "dodd": (42.2525, -71.8235, "Dodd Hall, Clark University"),
    "hughes": (42.2526, -71.8238, "Hughes Hall, Clark University"),
    
    "red square": (42.2512, -71.8230, "Red Square, Clark University"),
    "the quad": (42.2512, -71.8234, "The Quad, Clark University"),
    "online": (42.2510, -71.8232, "Virtual / Online Event"),
}

CLARK_LAT, CLARK_LON = 42.2510, -71.8232

def get_coordinates(address: str):
    address_lower = address.lower().strip()
    
    # 1. Match Shorthand
    for key, data in CAMPUS_LOCATIONS.items():
        if key in address_lower:
            return data

    # 2. Fallback to Geocoder for real addresses
    try:
        full_query = f"{address}, Worcester, MA"
        print(f"  [Geocoder] Looking up: {full_query}...")
        location = geolocator.geocode(full_query, timeout=2)
        print(f"      -> {location}")
        if location:
            # We return a formatted version of the address Google found
            return (location.latitude, location.longitude, f"{address}, Worcester, MA")
    except Exception:
        pass
    
    # 3. Final Fallback (Returns Center of Campus)
    return (CLARK_LAT, CLARK_LON, f"{address}, Clark University")
