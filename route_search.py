import requests

GOOGLE_API_KEY = 'AIzaSyAoH0BveJ2ra5H8osdVLkzTYAF2LHjbEe4'
endpoint = f'https://maps.googleapis.com/maps/api/directions/json?key={GOOGLE_API_KEY}'


class RouteSearch:
    def get_route_data(self, origin, destination):
        parameters = {
            'origin': origin,
            'destination': destination
        }
        response = requests.get(url=endpoint, params=parameters)
        response.raise_for_status()
        data = response.json()
        return data['routes'][0]['legs'][0]

    def reverse_geocode(self, latlon):
        """This method will take the lat/lon and return a nearby place"""
        reverse_geocode_endpoint = f'https://maps.googleapis.com/maps/api/geocode/json?latlng=' \
                                   f'{latlon}&result_type=LOCALITY&key={GOOGLE_API_KEY}'
        response = requests.get(url=reverse_geocode_endpoint)
        response.raise_for_status()
        rev_geocode_data = response.json()
        try:
            return rev_geocode_data['results'][0]['formatted_address']
        except IndexError:
            return rev_geocode_data['plus_code']['compound_code']
