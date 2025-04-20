from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz
import python_weather

def get_timezone(city):
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(city)
    if not location:
        raise ValueError("City not found")
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lat=location.latitude, lng=location.longitude)
    return pytz.timezone(timezone_str)

def get_local_time(city):
    tz = get_timezone(city)
    local_time = datetime.now(tz)
    return local_time.strftime('%I:%M %p'), local_time.strftime('%B %d, %Y')

async def get_weather(city: str) -> str:
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        weather = await client.get(city)
        return f"The current temperature in {city} is {weather.temperature}°F."
