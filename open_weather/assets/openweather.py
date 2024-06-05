import os
from typing import List
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
def current_weather_model(context: AssetExecutionContext, current_weather_slc: dict) -> List[pd.DataFrame]:
    """Transform the current weather data into data models."""
    current_weather_df = pd.json_normalize(current_weather_slc)
    
    # Extract the weather conditions as their own table
    weather_df = current_weather_df[['weather']].explode('weather')
    weather_conditions = pd.json_normalize(weather_df['weather'].to_list())

    # Explode the weather conditions into 1 row per weather condition in current weather table
    current_weather_df = current_weather_df.drop(columns=["weather"])
    current_weather_df = current_weather_df.merge(weather_conditions['id'].rename('weather_conditions_id'), left_index=True, right_index=True)

    context.add_output_metadata(
        {
            "current_weather_df": MetadataValue.md(current_weather_df.head().to_markdown()),
            "weather_conditions": MetadataValue.md(weather_conditions.head().to_markdown()),
        }
    )
    return [current_weather_df, weather_conditions]


@asset(group_name="openweather", compute_kind="Postgres")
def current_weather_models(current_weather_model: List[pd.DataFrame], postgres_resource: PostgresResource) -> None:
    """Load the data models into Postgres."""
    current_weather_model[0].to_sql("weather_raw", postgres_resource.get_engine(), if_exists='append', index=False)
    current_weather_model[1].to_sql("weather_conditions", postgres_resource.get_engine(), if_exists='append', index=False)


