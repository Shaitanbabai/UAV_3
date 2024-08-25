# паттерн Легковес

class DroneFlyweight:
    def __init__(self, model, manufacturer, sensors):
        self._model = model
        self._manufacturer = manufacturer
        self._sensors = sensors

    def operation(self, unique_state):
        print(f"""
        Дрон: модель {self._model}, производитель {self._manufacturer}
        Датчики: {self._sensors}
        Координаты: {unique_state["coordinates"]}
        Скорость: {unique_state["speed"]}
        Миссия: {unique_state["mission"]}
        Высота: {unique_state["altitude"]}
        Заряд батареи: {unique_state["battery"]}
""")

    @property
    def model(self):
        return self._model

    @property
    def manufacturer(self):
        return self._manufacturer

    @property
    def sensors(self):
        return self._sensors


class DroneFactory:
    def __init__(self):
        self._drones = {}

    def get_drone(self, model, manufacturer, sensors):
        key = (model, manufacturer, sensors)
        if key not in self._drones:
            self._drones[key] = DroneFlyweight(model, manufacturer, sensors)
        return self._drones[key]

    def list_drons(self):
        print(f"Всего дронов {len(self._drones)}")
        for key in self._drones:
            print(f"Ключ: модель {key[0]}, производитель {key[1]}, датчики {key[2]}")


def client_code():
    factory = DroneFactory()

    drone_1 = factory.get_drone("ModelX", "DroneCorp", "camera, GPS")
    drone_1.operation({
        "coordinates": "10, 20, 30",
        "speed": "50",
        "mission": "Surveillance",
        "altitude": "100",
        "battery": "80",
    })

    drone_2 = factory.get_drone("ModelX", "DroneCorp", "camera, GPS")
    drone_2.operation({
        "coordinates": "10, 20, 50",
        "speed": "49",
        "mission": "Surveillance",
        "altitude": "120",
        "battery": "85",
    })

    drone_3 = factory.get_drone("ModelY", "SkyTech", "lidar, GPS")
    drone_3.operation({
        "coordinates": "10, 20, 40",
        "speed": "52",
        "mission": "Surveillance",
        "altitude": "130",
        "battery": "81",
    })

    factory.list_drons()

if __name__ == "__main__":
    client_code()