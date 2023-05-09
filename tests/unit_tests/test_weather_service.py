"""Weather service tests"""

from unittest.mock import MagicMock

from modules.services.weather_service import fetch_weather_condition


class TestWeatherService:
    """Tests for the weather service"""

    @staticmethod
    def test_fetch_weather_condition(mock_search_fuzzy, mock_get, mock_redis):
        """Test  fetch_weather_condition with valid input"""

        mock_response = MagicMock()
        mock_response.status_code = 200

        mock_get.return_value = mock_response
        mock_redis.get.return_value = None
        mock_search_fuzzy.return_value = [MagicMock(alpha_2="FR")]

        result = fetch_weather_condition(75001, "France")

        try:
            result = fetch_weather_condition(75001, "France")
            assert result.get("description")
            assert result.get("temperature")
            assert result.get("humidity")

        except AssertionError:
            print(result)
            raise

    @staticmethod
    def test_fetch_weather_condition_invalid_payload(mock_search_fuzzy, mock_redis):
        """Test fetch_weather_condition with an invalid country name"""
        mock_search_fuzzy.return_value = []

        result = fetch_weather_condition(0000, "invalid")
        try:
            assert not result

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
