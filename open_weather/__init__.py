from dagster import (
    Definitions,
    EnvVar,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_package_module,
)

from open_weather.resources.open_weather_resource import OpenWeatherResource
from open_weather.resources.postgres_resource import PostgresResource

from . import assets

hourly_schedule = ScheduleDefinition(
    job=define_asset_job(name="current_weather_job"), cron_schedule="0 * * * *"
)

postgres_resource = PostgresResource(
                        host=EnvVar("PG_HOST"), 
                        dbname=EnvVar("PG_DBNAME"), 
                        user=EnvVar("PG_USER"),
                        password=EnvVar("PG_PASSWORD"),
                        port=EnvVar("PG_PORT"),
                    )

open_weather_resource = OpenWeatherResource(api_key=EnvVar("API_KEY"))

defs = Definitions(
    assets=load_assets_from_package_module(assets), 
    schedules=[hourly_schedule], 
    resources={"postgres_resource": postgres_resource,
               "open_weather_resource": open_weather_resource,}
)
