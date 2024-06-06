1. API Interaction:
- [x] Write a python script to interact with the OpenWeatherMap API.
- [x] Implement error handling and comply with the API's rate limits.
2. Data Extraction:
- [x] Extract weather forecast data at regular intervals.
- [ ] Handle potential connectivity issues or API downtimes.
- [x] Note: a few (10-20) api calls is fine here and be sure to stay well within the free tier of the api key.
3. Data Transformation:
- [x] Transform the JSON data into a format suitable for database storage.
- [x] Include necessary data cleaning and normalization steps.
4. Database Design:
- [x] Design a schema for the PostgreSQL database to store the weather data.
- [x] Consider appropriate data types, indexes, and constraints for the schema.
5. ETL Process:
- [x] Outline an ETL process that integrates extraction, transformation, and loading steps.
- [x] How would you orchestrate the workflow? Please outline the tech stack you would use.
- [x] Ensure the process is scalable and maintainable.
6. Logging and Monitoring:
- [x] Outline logging for tracking the pipeline's operations.
- [ ] Set up basic monitoring and alerts for the pipeline.
7. Testing:
- [ ] What unit tests for critical components of the pipeline would you consider?
- [ ] Note any testing strategies or frameworks utilized.
8. Deliverables:
- [x] Source code for the data pipeline.
- [x] Database schema (ERD).
- [x] Code can be in either notebook or script format.
- [ ] Outlines and documentation should be in a short presentation.
9. Evaluation Criteria:
- [ ] Code quality and clarity.
- [ ] Efficiency and scalability of the solution.
- [ ] Adherence to best practices in data engineering.


# Entity-Relationship Diagram (ERD)

## Entities and Attributes

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