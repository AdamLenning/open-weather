import pandas as pd
import requests
from dagster import AssetExecutionContext, MetadataValue, asset

from open_weather.resources.open_weather_resource import OpenWeatherResource
from open_weather.resources.postgres_resource import PostgresResource


@asset(group_name="openweather", compute_kind="OpenWeather API", ins={})
def current_weather_slc(
    context: AssetExecutionContext, open_weather_resource: OpenWeatherResource
) -> dict | None:
    """Get the current weather from the OpenWeather endpoint.

    API Docs: https://openweathermap.org/api/one-call-3#current
    """
    # Latitude and Longitude for SLC
    LAT = "40.760780"
    LON = "-111.891045"

    try:
        open_weather_url = open_weather_resource.get_url(LAT, LON)
        open_weather_response = requests.get(open_weather_url)
        open_weather_response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
        context.add_output_metadata(
            {
                "current_weather": open_weather_response.json(),
            }
        )
        return open_weather_response.json()
    except requests.exceptions.HTTPError as http_err:
        context.log.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        context.log.error(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        context.log.error(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        context.log.error(f"An error occurred: {req_err}")
    except Exception as err:
        context.log.error(f"An unexpected error occurred: {err}")


@asset(group_name="openweather", compute_kind="Pandas")
def current_weather_model(
    context: AssetExecutionContext, current_weather_slc: dict
) -> dict | None:
    """Transform the current weather data into data models."""
    try:
        # Normalize JSON data to a DataFrame
        current_weather_df = pd.json_normalize(current_weather_slc)

        # Extract the weather conditions as their own table
        weather_df = current_weather_df[["weather"]].explode("weather")
        weather_conditions = pd.json_normalize(weather_df["weather"].to_list())

        # Explode the weather conditions into 1 row per weather condition in the current weather table
        current_weather_df = current_weather_df.drop(columns=["weather"])
        current_weather_df = current_weather_df.merge(
            weather_conditions["id"].rename("weather_conditions_id"),
            left_index=True,
            right_index=True,
        )

        context.add_output_metadata(
            {
                "current_weather_df": MetadataValue.md(
                    current_weather_df.head().to_markdown()
                ),
                "weather_conditions": MetadataValue.md(
                    weather_conditions.head().to_markdown()
                ),
            }
        )
        return {
            "current_weather": current_weather_df,
            "weather_conditions": weather_conditions,
        }

    except KeyError as e:
        context.log.error(
            f"KeyError: {e} - Check if the required columns exist in the DataFrame"
        )
    except ValueError as e:
        context.log.error(f"ValueError: {e} - Check the data format")
    except Exception as e:
        context.log.error(f"An unexpected error occurred: {e}")


@asset(group_name="openweather", compute_kind="Postgres")
def current_weather_models(
    context: AssetExecutionContext,
    current_weather_model: dict,
    postgres_resource: PostgresResource,
) -> None:
    """Load the data models into Postgres."""
    try:
        for table_name, dataframe in current_weather_model.items():
            dataframe.to_sql(
                table_name,
                postgres_resource.get_engine(),
                if_exists="append",
                index=False,
            )
            context.log.info("Successfully inserted into weather_raw table.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
