average_speed = 60


class ListManager():
    def __init__(self, route_steps):
        self.route_steps = route_steps
        self.lon_list = []
        self.lat_list = []
        self.latlon_list = []
        self.city_list = []
        self.distance_list = []
        self.total_distance_list = []
        self.get_lists()
        self.get_total_distance_list()
        self.estimated_time_list = []
        self.estimate_time()
        self.weather_data_list = []
        self.route_length = len(route_steps)


    def get_lists(self):
        for step in self.route_steps:
            # Divided by 1609 to change the values of the distances from meters to miles
            self.distance_list.append(step['distance']['value'] / 1609)
            self.lat_list.append(step['end_location']['lat'])
            self.lon_list.append(step['end_location']['lng'])
        for x in range(len(self.lat_list)):
            self.latlon_list.append(str(self.lat_list[x]) + ', ' + str(self.lon_list[x]))


    def get_total_distance_list(self):
        for i in range(len(self.distance_list)):
            if i == 0:
                self.total_distance_list.append(self.distance_list[i])
            else:
                self.total_distance_list.append(self.distance_list[i] + self.total_distance_list[i - 1])

    def estimate_time(self):
        """estimates time passed based on distance traveled, assuming average travel speed of 60 mph"""
        x = 0
        for item in self.distance_list:
            x += item
            self.estimated_time_list.append(x/60)

    def refine_lists(self):
        """This formula will remove items from both coordinate lists if the distance/time
         hasn't been great enough to warrant a new weather check, and it will also insert items to
         the list if the distance between steps is large enough to warrant it"""


