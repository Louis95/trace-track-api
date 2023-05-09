from __future__ import annotations

import json
import logging

import pycountry
import requests
from requests import RequestException

from modules.utilities.configs import config

logger = logging.getLogger(__name__)


def fetch_weather_condition(zip_code: int, country: str) -> dict[str, str]:
    """Fetch the weather condition of a particular area.

    :param zip_code: the zipcode or postal code of the area
    :param country: the country
    :return: a dictionary containing information about the weather
    """
    return get_or_update_weather_from_cache(zip_code, country)


def get_country_code(country_name) -> str | None:
    """Returns the country code of a given country.

    Eg returns FR for France.

    :param country_name: country name
    :return: the country code.
    """
    try:
        country = pycountry.countries.search_fuzzy(country_name)[0]
        return country.alpha_2
    except LookupError:
        logger.error("Unable to fetch country code from given country")
        return None


def get_or_update_weather_from_cache(zip_code: int, country: str) -> dict:
    """Get or update the weather information from cache.

    :param country: the country code.
    :param zip_code:  the zip code
    :return: the weather information from cache
    """

    try:
        country_code = get_country_code(country)

        weather_info = config.cache.get(zip_code)
        if weather_info:
            return json.loads(weather_info)

        params = {
            "zip": f"{zip_code},{country_code}",
            "appid": config.WEATHER_API_KEY,
            "units": "imperial",
        }

        response = requests.get(config.WEATHER_API_URL, params=params)
        if response.status_code == 200:
            logger.info("Successfully fetched weather information")
            weather_information_response = response.json()

            weather_data = {
                "description": weather_information_response["weather"][0][
                    "description"
                ],
                "temperature": weather_information_response["main"]["temp"],
                "humidity": weather_information_response["main"]["humidity"],
            }

            config.cache.setex(zip_code, 7200, json.dumps(weather_data))

            return weather_data

    except RequestException:
        logger.error("An error occurred while trying to get weather information.")
        return {"description": "unknown", "temperature": None, "humidity": None}
