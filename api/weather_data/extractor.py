import os

import requests
import os

class WeatherProducer(object):
    """Get weather data from external API."""

    def __init__(self):
        self.url = os.environ.get('SOURCE_HOST', 'https://api.openweathermap.org/data/2.5/weather')
        self.api_key = os.environ.get('API_KEY', 'b3cead5de55dc7c37b8a59412f5a4fc0')

    def get_weather_data(self, city, units='metric'):
        payload = {'q': city, 'appid': self.api_key, 'units': units}
        headers = {}
        response = requests.request('GET', self.url, headers=headers, params=payload)
        return response.json()
