from geopy.geocoders import GoogleV3
from geopy.distance import vincenty
from alexi.geo.config import GOOGLE_GEO_API_KEY, REGION_CODE, LANGUAGE

_client = GoogleV3(api_key=GOOGLE_GEO_API_KEY)

def geocode(address):
    global _client
    result = _client.geocode(address, region=REGION_CODE, language=LANGUAGE, exactly_one=True)
    return result.latitude, result.longitude, result.address

def reverse(latitude, longitude):
    global _client
    result = _client.reverse([latitude, longitude], language=LANGUAGE, exactly_one=True)
    return result.address

def distance(points):
    # Return the distance along a route made up of "points" (lat/lng)
    return sum(map(lambda p: vincenty(*p).kilometers, zip(points, points[1:])))