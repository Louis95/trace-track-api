from modules.services.weather_service import fetch_weather_condition


class TestWeatherService:
    @staticmethod
    def test_fetch_weather_condition():
        """Test  fetch_weather_condition with valid input"""

        result = fetch_weather_condition(1016, "Netherlands")

        try:
            assert result
            assert result["description"]
            assert result["temperature"]
            assert result["humidity"]

        except AssertionError:
            print(result)
            raise

    @staticmethod
    def test_fetch_weather_condition_with_invalid_country() -> None:
        """Test fetch_weather_condition with invalid country"""
        result = fetch_weather_condition(1016, "invalid-country")

        try:
            assert result["description"] == "unknown"
            assert not result["temperature"]
            assert not result["humidity"]

        except AssertionError:
            print(result)
            raise
