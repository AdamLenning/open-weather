# Table of Contents
- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
- [Getting Started](#getting-started)
- [Tech Stack](#tech-stack)
- [Schedules](#schedules)
- [Data Sources](#data-sources)
- [Data Model/Transformations](#data-modeltransformations)
  - [Entity-Relationship Diagram (ERD)](#entity-relationship-diagram-erd)
    - [current\_weather](#current_weather)
    - [weather\_conditions](#weather_conditions)
  - [Relationships](#relationships)
- [Data Destinations](#data-destinations)
- [Logging and Monitoring](#logging-and-monitoring)
- [Testing](#testing)


# Introduction
This is a basic Dagster project that pulls data from the Open Weather API and loads it into a Postgres database.

# Getting Started
1. Clone this repo
2. Create a virtual environment and run `pip install -e ".[dev]"`
3. Run `dagster dev` and you are off to the races!

# Tech Stack
- Dagster for Orchestration and Transformations
- Pytest for testing
- Postgres for Storage
- Dagster + Slack for notifications and monitoring

# Schedules
- An hourly schedule is written so as to not consume too much quota from the API.

# Data Sources
- Data is pulled from the [Open Weather API](https://openweathermap.org/api/one-call-3#current).
- You will need to make an API key to get data from the API.
- The Dagster asset is configured to pull data for Salt Lake City, though this can be easily changed for different latitudes and longitudes.

# Data Model/Transformations
## Entity-Relationship Diagram (ERD)

### current_weather
- **base**: VARCHAR
- **visibility**: INTEGER
- **dt**: INTEGER
- **timezone**: INTEGER
- **id**: INTEGER (Primary Key)
- **name**: VARCHAR
- **cod**: INTEGER
- **coord_lon**: FLOAT
- **coord_lat**: FLOAT
- **main_temp**: FLOAT
- **main_feels_like**: FLOAT
- **main_temp_min**: FLOAT
- **main_temp_max**: FLOAT
- **main_pressure**: INTEGER
- **main_humidity**: INTEGER
- **wind_speed**: FLOAT
- **wind_deg**: INTEGER
- **clouds_all**: INTEGER
- **sys_type**: INTEGER
- **sys_id**: INTEGER
- **sys_country**: VARCHAR
- **sys_sunrise**: INTEGER
- **sys_sunset**: INTEGER
- **weather_conditions_id**: INTEGER (Foreign Key to Weather_Conditions)

### weather_conditions
- **id**: INTEGER (Primary Key)
- **main**: VARCHAR
- **description**: VARCHAR
- **icon**: VARCHAR

## Relationships

- **Weather_Base** has a many-to-one relationship with **Weather_Conditions** (indicated by `weather_conditions_id`).
  
# Data Destinations
- Data is loaded into a Postgres Database.
- In development, a local docker instance of Postgres was used, but you can simply swap out the environment variables to hit production databases.
- Data is writting in append mode. This may present challenges on the weather_conditions table which is meant to be a dimension table with fewer writes. Upsert is the ideal, but not used in this pipelines.

# Logging and Monitoring
- A basic slack sensor is written and added to the definitions when a job fails. If choosing to deploy this with Dagster+ I would opt for the built in notifications and alerting with Dagster.
- All logs are sent to the Dagster webserver.
  
# Testing
- Unit Tests for each asset are stubbed out and expected to be implemented with pytest.
