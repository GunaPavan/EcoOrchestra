# src/ecoorchestra/data/fetcher.py

import requests
import os
import logging
from dotenv import load_dotenv
from typing import Optional
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


def get_weather_data(city: str, country: str = "IN", retries: int = 3) -> Optional[WeatherData]:
    """
    Fetch temperature, humidity, and wind speed from OpenWeatherMap.
    Returns None if API fails.
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={OWM_API_KEY}&units=metric"
    for attempt in range(1, retries + 1):
        try:
            res = requests.get(url, timeout=10)
            res.raise_for_status()
            data = res.json()

            return WeatherData(
                temperature=data["main"]["temp"],
                humidity=data["main"]["humidity"],
                wind_speed=data["wind"]["speed"]
            )
        except Exception as e:
            logger.warning(f"[Attempt {attempt}] Failed to fetch weather data: {e}")
    return None


def get_aqi_data(city: str, state: str = "Delhi", country: str = "India", retries: int = 3) -> Optional[AQIData]:
    """
    Fetch AQI data from IQAir (AirVisual). Returns None if API fails.
    """
    url = f"http://api.airvisual.com/v2/city?city={city}&state={state}&country={country}&key={AIRVISUAL_API_KEY}"
    for attempt in range(1, retries + 1):
        try:
            res = requests.get(url, timeout=10)
            res.raise_for_status()
            data = res.json()

            return AQIData(
                aqi=data["data"]["current"]["pollution"]["aqius"]
            )
        except Exception as e:
            logger.warning(f"[Attempt {attempt}] Failed to fetch AQI data: {e}")
    return None
