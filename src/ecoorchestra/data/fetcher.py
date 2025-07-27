# src/ecoorchestra/data/fetcher.py

import os
import logging
import requests
from dotenv import load_dotenv
from typing import Optional, Dict
from dataclasses import dataclass

load_dotenv()

OWM_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
AIRVISUAL_API_KEY = os.getenv("AIRVISUAL_API_KEY")

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@dataclass
class WeatherData:
    temperature: float
    humidity: float
    wind_speed: float

@dataclass
class AQIData:
    aqi: int

@dataclass
class Location:
    city: str
    state: Optional[str] = None
    country: str = "India"

def get_weather_data(location: Location, retries: int = 3) -> Optional[WeatherData]:
    """
    Fetch temperature, humidity, and wind speed from OpenWeatherMap API.
    """
    url = (
        f"http://api.openweathermap.org/data/2.5/weather?"
        f"q={location.city},{location.country}&appid={OWM_API_KEY}&units=metric"
    )

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return WeatherData(
                temperature=data["main"]["temp"],
                humidity=data["main"]["humidity"],
                wind_speed=data["wind"]["speed"]
            )
        except Exception as e:
            logger.warning(f"[Weather Attempt {attempt}] Failed: {e}")
    return None

def get_aqi_data(location: Location, retries: int = 3) -> Optional[AQIData]:
    """
    Fetch AQI data from AirVisual (IQAir) API.
    Requires city, state, and country.
    """
    if not location.state:
        logger.warning("❗ Cannot fetch AQI without `state`. Skipping AQI.")
        return None

    url = (
        f"http://api.airvisual.com/v2/city?"
        f"city={location.city}&state={location.state}&country={location.country}&key={AIRVISUAL_API_KEY}"
    )

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return AQIData(aqi=data["data"]["current"]["pollution"]["aqius"])
        except Exception as e:
            logger.warning(f"[AQI Attempt {attempt}] Failed: {e}")
    return None

def fetch_environment_data(city: str, state: Optional[str] = None, country: str = "India") -> Dict[str, float]:
    """
    Aggregates dynamic weather and AQI data into a dictionary.
    Raises RuntimeError if critical data is missing.
    """
    location = Location(city=city, state=state, country=country)
    logger.info(f"🌍 Fetching environmental data for: {location}")

    weather = get_weather_data(location)
    aqi = get_aqi_data(location)

    if not weather:
        raise RuntimeError("❌ Failed to fetch weather data.")

    result = {
        "temperature": weather.temperature,
        "humidity": weather.humidity,
        "wind_speed": weather.wind_speed
    }

    if aqi:
        result["aqi"] = aqi.aqi
    else:
        result["aqi"] = -1  # Optional: use sentinel value for missing AQI

    logger.info(f"✅ Fetched environmental data: {result}")
    return result
