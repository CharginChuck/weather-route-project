import requests
import json

WEATHER_API_KEY = '69f04e4613056b159c2761a9d9e664d2'

URL = 'https://api.openweathermap.org/data/2.5/onecall'
# 'lat': 35.151409,
# 'lon': -85.222191,
class Weather:
    def weather_search(self, lat, lon):
        weather_params = {
            'lat': lat,
            'lon': lon,
            'appid': WEATHER_API_KEY,
            'units': 'imperial',
            'exclude': 'current,minutely,daily',
        }

        response = requests.get(url=URL, params=weather_params)
        response.raise_for_status()
        data = response.json()
        hourly_data = data['hourly']
        with open('weather_data.json', 'w') as file:
            json.dump(data, file, indent=4)
        return hourly_data
