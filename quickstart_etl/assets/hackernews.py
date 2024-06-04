import base64
from io import BytesIO
import os
from typing import List

import matplotlib.pyplot as plt
import pandas as pd
import requests
from dagster import AssetExecutionContext, MetadataValue, asset
from wordcloud import STOPWORDS, WordCloud


@asset(group_name="openweather", compute_kind="OpenWeather API")
def current_weather_london(context: AssetExecutionContext) -> dict:
    """Get up to 500 top stories from the HackerNews topstories endpoint.

    API Docs: https://github.com/HackerNews/API#new-top-and-best-stories
    """
    API_KEY = os.getenv("API_KEY")
    context.log.info(API_KEY)
    open_weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat=40.760780&lon=-111.891045&appid={API_KEY}"
    current_weather = requests.get(open_weather_url).json()

    context.log.info(current_weather)

    return current_weather



@asset(group_name="openweather", compute_kind="Plot")
def hackernews_topstories_word_cloud(
    context: AssetExecutionContext, current_weather_london: pd.DataFrame
) -> bytes:
    """Exploratory analysis: Generate a word cloud from the current top 500 HackerNews top stories.
    Embed the plot into a Markdown metadata for quick view.

    Read more about how to create word clouds in http://amueller.github.io/word_cloud/.
    """
    stopwords = set(STOPWORDS)
    stopwords.update(["Ask", "Show", "HN"])
    titles_text = " ".join([str(item) for item in current_weather_london["title"]])
    titles_cloud = WordCloud(stopwords=stopwords, background_color="white").generate(titles_text)

    # Generate the word cloud image
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(titles_cloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)

    # Save the image to a buffer and embed the image into Markdown content for quick view
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    image_data = base64.b64encode(buffer.getvalue())
    md_content = f"![img](data:image/png;base64,{image_data.decode()})"

    # Attach the Markdown content as metadata to the asset
    # Read about more metadata types in https://docs.dagster.io/_apidocs/ops#metadata-types
    context.add_output_metadata({"plot": MetadataValue.md(md_content)})

    return image_data
