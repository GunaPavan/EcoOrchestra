# tests/test_fetcher.py
import pytest
import logging
from unittest.mock import patch, Mock
from ecoorchestra.data.fetcher import (
    fetch_environment_data,
    WeatherData,
    AQIData,
    Location,
    get_weather_data,
    get_aqi_data
)

# Sample test data
SAMPLE_WEATHER_RESPONSE = {
    "main": {"temp": 25.5, "humidity": 60},
    "wind": {"speed": 3.2}
}

SAMPLE_AQI_RESPONSE = {
    "data": {
        "current": {
            "pollution": {"aqius": 42}
        }
    }
}

# ---- Test Location Dataclass ----
def test_location_dataclass():
    loc = Location(city="Mumbai", state="Maharashtra", country="India")
    assert loc.city == "Mumbai"
    assert loc.state == "Maharashtra"
    assert loc.country == "India"

# ---- Test Weather Data Fetching ----
@patch('requests.get')
def test_get_weather_data_success(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = SAMPLE_WEATHER_RESPONSE
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    location = Location(city="Delhi", country="India")
    result = get_weather_data(location)

    assert result.temperature == 25.5
    assert result.humidity == 60
    assert result.wind_speed == 3.2

@patch('requests.get')
def test_get_weather_data_failure(mock_get):
    mock_get.side_effect = Exception("API timeout")
    location = Location(city="Delhi", country="India")
    assert get_weather_data(location) is None

# ---- Test AQI Data Fetching ----
@patch('requests.get')
def test_get_aqi_data_success(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = SAMPLE_AQI_RESPONSE
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    location = Location(city="Bangalore", state="Karnataka", country="India")
    result = get_aqi_data(location)

    assert result.aqi == 42

@patch('requests.get')
def test_get_aqi_data_missing_state(mock_get, caplog):
    caplog.set_level(logging.WARNING)
    location = Location(city="Chennai", country="India")
    assert get_aqi_data(location) is None
    assert "Cannot fetch AQI without `state`" in caplog.text

# ---- Test Integrated Fetch Function ----
@patch('ecoorchestra.data.fetcher.get_weather_data')
@patch('ecoorchestra.data.fetcher.get_aqi_data')
def test_fetch_environment_data_success(mock_aqi, mock_weather, caplog):
    caplog.set_level(logging.INFO)

    mock_weather.return_value = WeatherData(25.5, 60, 3.2)
    mock_aqi.return_value = AQIData(42)

    result = fetch_environment_data("Pune", "Maharashtra", "India")

    assert result["temperature"] == 25.5
    assert result["aqi"] == 42

    # Check for log message in a more robust way
    log_messages = [record.message for record in caplog.records]
    assert any("Fetched environmental data" in message for message in log_messages)

@patch('ecoorchestra.data.fetcher.get_weather_data')
def test_fetch_environment_data_weather_failure(mock_weather):
    mock_weather.return_value = None

    with pytest.raises(RuntimeError) as excinfo:
        fetch_environment_data("Hyderabad", "Telangana")
    assert "Failed to fetch weather data" in str(excinfo.value)

# ---- Test Retry Logic ----
@patch('requests.get')
def test_weather_retry_logic(mock_get):
    mock_get.side_effect = [
        Exception("First fail"),
        Exception("Second fail"),
        Mock(json=lambda: SAMPLE_WEATHER_RESPONSE)
    ]

    location = Location(city="Jaipur", country="India")
    result = get_weather_data(location, retries=3)
    assert result.temperature == 25.5
    assert mock_get.call_count == 3
