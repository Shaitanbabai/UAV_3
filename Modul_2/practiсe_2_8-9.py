# паттерн Легковес

class DroneFlyweight:
    def __init__(self, model, manufacturer, sensors):
        self._model = model
        self._manufacturer = manufacturer
        self._sensors = sensors

    def operation(self, unique_state):
        print(f"""
        ===============
        Дрон
            Модель: {self._model}
            Производитель: {self._manufacturer}
            Датчики: {self._sensors}

        Текущие параметры
            Координаты: {unique_state["coordinates"]}
            Скорость: {unique_state["speed"]}
            Миссия: {unique_state["mission"]}
            Высота: {unique_state["altitude"]}
            Заряд батареи: {unique_state["battery"]}
        """)

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    @property
    def manufacturer(self):
        return self._manufacturer

    @manufacturer.setter
    def manufacturer(self, value):
        self._manufacturer = value

    @property
    def sensors(self):
        return self._sensors

    @sensors.setter
    def sensors(self, value):
        self._sensors = value


class DroneFactory:
    def __init__(self):
        # Хранилище объектов DroneFlyweight для предотвращения создания дублирующих объектов
        self._drones = {}

    def get_drone(self, model, manufacturer, sensors):
        # Создаем уникальный ключ для идентификации дрона по его свойствам
        key = (model, manufacturer, sensors)
        # Если дрон с такими характеристиками еще не создан, создаем его и добавляем в хранилище
        if key not in self._drones:
            self._drones[key] = DroneFlyweight(model, manufacturer, sensors)
        # Возвращаем существующий или вновь созданный объект дрона
        return self._drones[key]

    def list_drones(self):
        # Выводим информацию о количестве и характеристиках всех созданных объектов дронов
        print(f"Всего легковесных дронов: {len(self._drones)}")
        for value in self._drones.keys():
            model, manufacturer, sensors = value
            print(f"Ключ: модель {model}, производитель {manufacturer}, сенсоры {sensors}")


def client_code():
    factory = DroneFactory()

    # Создаем несколько дронов и используем их, задавая уникальные состояния
    drone_1 = factory.get_drone("ModelX", "DroneCorp", "camera, GPS")
    drone_1.operation({
        "coordinates": "10, 20",
        "speed": "50",
        "mission": "surveillance",
        "altitude": "100",
        "battery": "80",
    })

    drone_2 = factory.get_drone("ModelX", "DroneCorp", "camera, GPS")
    drone_2.operation({
        "coordinates": "110, 120",
        "speed": "60",
        "mission": "surveillance",
        "altitude": "130",
        "battery": "82",
    })

    drone_3 = factory.get_drone("ModelY", "SkyTech", "camera, GPS, lidar")
    drone_3.operation({
        "coordinates": "101, 201",
        "speed": "70",
        "mission": "surveillance",
        "altitude": "120",
        "battery": "81",
    })

    factory.list_drones()


if __name__ == '__main__':
    client_code()
