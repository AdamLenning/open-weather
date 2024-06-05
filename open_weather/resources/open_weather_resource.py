from dagster import ConfigurableResource


class OpenWeatherResource(ConfigurableResource):
    api_key: str

    def get_url(self, lat: str, lon: str):
        return f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.api_key}"
