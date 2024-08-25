import random


class GPS:
    def __init__(self, init_coordinates=(0.0, 0.0)):
        self.coordinates = init_coordinates

    def update_coordinates(self):
        """
        Симулирует обновление координат GPS
        """
        # lat = round(random.uniform(1, 50), 4) # широта
        # lon = round(random.uniform(1, 50), 4) # долгота
        lat_variation = random.uniform(-0.0001, 0.0001)  # изменение широты
        lon_variation = random.uniform(-0.0001, 0.0001)  # изменение долготы
        lat = round(self.coordinates[0] + lat_variation, 4)
        lon = round(self.coordinates[1] + lon_variation, 4)
        self.coordinates = (lat, lon)
        # print(f"Обновленные коодинат: {self.coordinates}")
        return self.coordinates


class DistanceSensor:
    def __init__(self, max_dist=10000.0):
        self.max_dist = max_dist
        self.cur_dist = self.update_dist()

    def update_dist(self):
        """
        Симулируем измерение расстояния
        """
        return random.uniform(0, self.max_dist)

    def get_dist(self):
        print(self.cur_dist)
        return self.cur_dist



if __name__ == "__main__":
    gps_module = GPS((55.7558, 37.6176))
    print(gps_module.coordinates)
    # for i in (0, 1, 2, 3):
    for i in range(10000):
        gps_module.update_coordinates()
    print(gps_module.coordinates)




