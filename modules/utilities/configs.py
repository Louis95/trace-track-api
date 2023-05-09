import os

import redis as redis
from dotenv import load_dotenv

load_dotenv()


class Config:
    WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
    WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")
    cache = redis.Redis(host="localhost", port=6379, db=0)


config = Config()
