from setuptools import find_packages, setup

setup(
    name="open_weather",
    packages=find_packages(exclude=["open_weather_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "boto3",
        "pandas",
        "matplotlib",
        "textblob",
        "tweepy",
        "wordcloud",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
