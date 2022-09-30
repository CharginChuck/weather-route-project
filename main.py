from route_search import RouteSearch
import json
from list_manager import ListManager
from weather import Weather
from datetime import datetime, timedelta

origin = input('Enter origin (e.g. Atlanta, GA): ')
destination = input('Enter destination (e.g. Portland, ME) :')
hours_to_departure = int(input('In how many hours will you leave? '))

# RouteSearch uses Google Maps Directions API to pull route data for the defined origin and destination
rs = RouteSearch()
route_data = rs.get_route_data(origin=origin, destination=destination)
route_steps = route_data['steps']

# Below is temporary just to help visualize and work with the json data
with open('json/route_data.json', 'w') as file:
    json.dump(obj=route_steps, fp=file, indent=4)

lm = ListManager(route_steps=route_steps)

# Add the weather data for each endpoint in each step of the route steps to the list lm.weather_data_list
weather = Weather()
for x in range(len(route_steps)):
    lm.weather_data_list.append(weather.weather_search(lat=lm.lat_list[x], lon=lm.lon_list[x]))

# Round the estimated time list
rounded_time = [round(time) for time in lm.estimated_time_list]
# Add hours to departure to each item in rounded time
rounded_time_plus_hours_to_departure = [time + hours_to_departure for time in rounded_time]
# Feed the new list back into the list manager
lm.estimated_time_list = rounded_time_plus_hours_to_departure

# print()
# print(lm.latlon_list)
# print(len(lm.latlon_list))


# Populate the city list
# for x in range(len(lm.latlon_list)):
#     lm.city_list.append(rs.reverse_geocode(lm.latlon_list[x]))
# print(lm.city_list)


# This boolean will be set to False if there is any inclement weather found throughout the trip
no_rain = True
# Check each step for inclement weather at estimated time
"""I moved the reverse geocode search in here instead of pre-searching and populating the city list above 
to reduce the amount of geocoding requests the program was making"""

now = datetime.now()
for x in range(lm.route_length):
    weather_description = lm.weather_data_list[x][lm.estimated_time_list[x]]['weather'][0]['description']
    time_at_route_step = now + timedelta(hours=lm.estimated_time_list[x])
    time_at_route_step = time_at_route_step.strftime('%I:%M %p')
    if 'rain' in weather_description or 'snow' in weather_description:
        no_rain = False
        city = rs.reverse_geocode(lm.latlon_list[x])
        print(f'Weather forecast for {city} looks like {weather_description} at around {time_at_route_step}')

if no_rain == True:
    print("After searching through your route, we haven't found any inclement weather.  Have a great trip! :)")
