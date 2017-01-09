from geopy.geocoders import GoogleV3
from alexi.geo.config import GOOGLE_GEO_API_KEY, REGION_CODE, LANGUAGE

_client = GoogleV3(api_key=GOOGLE_GEO_API_KEY)

def geocode(address):
    global _client

    result = _client.geocode(address, region=REGION_CODE, language=LANGUAGE)
    return result.latitude, result.longitude, result.address

def reverse(latitude, longitude):
    global _client
    result = _client.reverse([latitude, longitude], language=LANGUAGE)
    return result.address