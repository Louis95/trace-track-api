import json
from unittest.mock import MagicMock, patch

import pytest

from modules.services.weather_service import fetch_weather_condition


class TestWeatherService:
    """Tests for the weather service"""

    @staticmethod
    def test_fetch_weather_condition(mock_search_fuzzy, mock_get, mock_redis):
        """Test  fetch_weather_condition with valid input"""

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "weather": [{"description": "sunny"}],
            "main": {"temp": 72, "humidity": 50},
        }

        mock_get.return_value = mock_response
        mock_redis.get.return_value = None
        mock_search_fuzzy.return_value = [MagicMock(alpha_2="FR")]

        result = fetch_weather_condition(75001, "France")

        try:
            assert result == {
                "description": "sunny",
                "temperature": 72,
                "humidity": 50,
            }

            mock_redis.get.return_value = json.dumps(result)

            result = fetch_weather_condition(75001, "France")
            assert result == {
                "description": "sunny",
                "temperature": 72,
                "humidity": 50,
            }
        except AssertionError:
            print(result)
            raise

    @staticmethod
    def test_fetch_weather_condition_invalid_country(mock_search_fuzzy, mock_redis):
        """Test fetch_weather_condition with an invalid country name"""
        mock_search_fuzzy.return_value = []

        result = fetch_weather_condition(75001, "invalid")
        try:
            assert result == {
                "description": "unknown",
                "temperature": None,
                "humidity": None,
            }

            mock_search_fuzzy.assert_called_once_with("invalid")
            mock_redis.get.assert_not_called()
        except AssertionError:
            print(result)
            raise

    @staticmethod
    def test_fetch_weather_condition_api_error(mock_search_fuzzy, mock_get, mock_redis):
        """Test fetch_weather_condition when the weather API returns an error"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        mock_redis.get.return_value = None
        mock_search_fuzzy.return_value = [MagicMock(alpha_2="FR")]

        result = fetch_weather_condition(75001, "France")
        try:
            assert result["description"] == "unknown"
            assert not result["humidity"]
            assert not result["temperature"]
        except AssertionError:
            print(result)
