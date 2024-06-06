import os

from dagster import (
    Definitions,
    EnvVar,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_package_module,
)
from dagster_slack import make_slack_on_run_failure_sensor

from open_weather.resources.open_weather_resource import OpenWeatherResource
from open_weather.resources.postgres_resource import PostgresResource

from . import assets

# Hourly Schedule
hourly_schedule = ScheduleDefinition(
    job=define_asset_job(name="current_weather_job"), cron_schedule="0 * * * *"
)

# Resources
postgres_resource = PostgresResource(
    host=EnvVar("PG_HOST"),
    dbname=EnvVar("PG_DBNAME"),
    user=EnvVar("PG_USER"),
    password=EnvVar("PG_PASSWORD"),
    port=EnvVar("PG_PORT"),
)
open_weather_resource = OpenWeatherResource(api_key=EnvVar("API_KEY"))

# Run failure sensor, may be used when Dagster+ is not configured for Slack Notifications
slack_on_run_failure = make_slack_on_run_failure_sensor(
    channel="#my_channel",
    slack_token=os.getenv("MY_SLACK_TOKEN", "Token Not Found"),
    text_fn=lambda context: f"Job {context.dagster_run.job_name} failed with Error: {context.failure_event.message}",
)

defs = Definitions(
    assets=load_assets_from_package_module(assets),
    schedules=[hourly_schedule],
    sensors=[slack_on_run_failure],
    resources={
        "postgres_resource": postgres_resource,
        "open_weather_resource": open_weather_resource,
    },
)
