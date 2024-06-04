import os
from typing import List

import pandas as pd
import requests
from dagster import AssetExecutionContext, asset


@asset(group_name="openweather", compute_kind="OpenWeather API")
def current_weather_slc(context: AssetExecutionContext) -> dict:
    """Get the current weather from the OpenWeather endpoint.

    API Docs: https://openweathermap.org/api/one-call-3#current
    """
    API_KEY = os.getenv("API_KEY")
    open_weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat=40.760780&lon=-111.891045&appid={API_KEY}"
    current_weather = requests.get(open_weather_url).json()

    context.log.info(current_weather)

    return current_weather


@asset(group_name="openweather", compute_kind="Pandas")
def current_weather_transformations(current_weather_slc: dict) -> List[pd.DataFrame]:
    """Transform the current weather data into data models."""
    return [pd.DataFrame()]


@asset(group_name="openweather", compute_kind="Postgres")
def current_weather_models(current_weather_transformations: List[pd.DataFrame]) -> None:
    """Load the data models into Postgres."""
    pass
