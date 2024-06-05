import os
import pandas as pd
import requests
from dagster import AssetExecutionContext, MetadataValue, asset

from open_weather.resources.open_weather_resource import OpenWeatherResource
from open_weather.resources.postgres_resource import PostgresResource


@asset(group_name="openweather", compute_kind="OpenWeather API", ins={})
def current_weather_slc(context: AssetExecutionContext, open_weather_resource: OpenWeatherResource) -> dict:
    """Get the current weather from the OpenWeather endpoint.

    API Docs: https://openweathermap.org/api/one-call-3#current
    """
    # Latitude and Longitude for SLC
    LAT = "40.760780" 
    LON = "-111.891045"

    open_weather_url = open_weather_resource.get_url(LAT, LON)
    open_weather_response = requests.get(open_weather_url)
    context.log.info(f"OpenWeather Response: {open_weather_response}")

    context.add_output_metadata(
        {
            "current_weather": open_weather_response.json(),
        }
    )

    return open_weather_response.json()


@asset(group_name="openweather", compute_kind="Pandas")
def current_weather_model(context: AssetExecutionContext, current_weather_slc: dict) -> pd.DataFrame:
    """Transform the current weather data into data models."""
    current_weather_df = pd.json_normalize(current_weather_slc)
    context.add_output_metadata(
        {
            "preview": MetadataValue.md(current_weather_df.head().to_markdown()),
        }
    )
    return current_weather_df


@asset(group_name="openweather", compute_kind="Postgres")
def current_weather_models(current_weather_model: pd.DataFrame, postgres_resource: PostgresResource) -> None:
    """Load the data models into Postgres."""
    current_weather_model.to_sql("table_name", postgres_resource.get_engine(), if_exists='append', index=False)

