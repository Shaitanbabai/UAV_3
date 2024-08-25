# Фабричный метод

class Sensor:
    def get_data(self):
        pass

class Camera(Sensor):
    def get_data(self):
        return "Данные с камеры"

class Lidar(Sensor):
    def get_data(self):
        return "Данные с лидара"

# Базовый класс для фабрик, создающих датчики
class SensorFactory:
    def create_sensor(self):
        pass

# Фабрика для создания объектов класса Camera
class CameraFactory(SensorFactory):
    def create_sensor(self):
        return Camera()

# Фабрика для создания объектов класса Lidar
class LidarFactory(SensorFactory):
    def create_sensor(self):
        return Lidar()

# Используем фабрику для создания камеры и получения данных
sensor_factory = CameraFactory()
sensor = sensor_factory.create_sensor()
data = sensor.get_data()
print(data)
