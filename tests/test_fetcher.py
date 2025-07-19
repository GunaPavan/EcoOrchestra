# tests/test_fetcher.py

from ecoorchestra.data.fetcher import get_weather_data, get_aqi_data, WeatherData, AQIData


def test_weather_fetch():
    result = get_weather_data("Delhi")
    assert isinstance(result, WeatherData), "Expected WeatherData object"
    assert isinstance(result.temperature, (int, float)), "Temperature must be a number"
    assert isinstance(result.humidity, (int, float)), "Humidity must be a number"
    assert isinstance(result.wind_speed, (int, float)), "Wind speed must be a number"


def test_aqi_fetch():
    result = get_aqi_data("Delhi")
    assert isinstance(result, AQIData), "Expected AQIData object"
    assert isinstance(result.aqi, int), "AQI must be an integer"
    assert 0 <= result.aqi <= 500, "AQI should be in valid range"
