# Single Responsibility Principle (Принцип единственной ответственности)

class NavigationSystem:
    def calc_route(self, start, end):
        print(f"Расчет маршрута от {start} до {end}")
        # Логика расчета маршрута
        pass

class CommunicationSystem:
    def send_data(self, data):
        print(f"Отправка данных: {data}")
        # Логика отправки данных
        pass

# В этом примере классы NavigationSystem и CommunicationSystem имеют четко определенные обязанности.
# NavigationSystem отвечает только за расчеты маршрутов, а CommunicationSystem - за отправку данных.

# Open/Closed Principle (Принцип открытости/закрытости)

from abc import ABC, abstractmethod

# Абстрактный базовый класс для всех режимов полета
class FlightMode(ABC):
    @abstractmethod
    def execute(self):
        pass

# Конкретные режимы полета, наследующие абстрактный класс FlightMode
class ManualMode(FlightMode):
    def execute(self):
        print("Ручной режим управления")
        # Логика ручного управления
        pass

class AutoMode(FlightMode):
    def execute(self):
        print("Режим управления автопилот")
        # Логика автопилота
        pass

class EmergencyMode(FlightMode):
    def execute(self):
        print("Аварийный режим")
        # Логика аварийного режима
        pass

class DestructionMode(FlightMode):
    def execute(self):
        print("САМОЛИКВИДАЦИЯ!")
        # Логика самоуничтожения
        pass

# Класс Drone использует режимы полета, соблюдая принцип открытости/закрытости
class Drone:
    def __init__(self, mode: FlightMode):
        self.__mode = mode

    def change_mode(self, mode: FlightMode):
        self.__mode = mode

    def fly(self):
        self.__mode.execute()

# Пример использования принципа открытости/закрытости:
manual_mode = ManualMode()
destruction_mode = DestructionMode()

drone = Drone(manual_mode)
drone.fly()
drone.change_mode(destruction_mode)
drone.fly()
print("\n ================ \n")

# Принцип подстановки Лисков (Liskov Substitution Principle)

# Абстрактный класс для различных типов сенсоров
class Sensor(ABC):
    @abstractmethod
    def get_data(self):
        pass

# Классы конкретных сенсоров, наследующие Sensor и реализующие метод get_data
class Camera(Sensor):
    def get_data(self):
        print("Получение видео с камеры")
        return "Данные с камеры"

class Lidar(Sensor):
    def get_data(self):
        print("Чтение данных с лидара")
        return "Данные с лидара"

class Battery(Sensor):
    def get_data(self):
        print("Чтение уровня заряда")
        return "Данные с батареи"

# Класс Drone2 использует сенсоры, которые реализуют общий интерфейс Sensor
class Drone2:
    def __init__(self, sensor: Sensor):
        self.__sensor = sensor

    def gather_data(self):
        data = self.__sensor.get_data()
        print(f"Собранные данные: {data}")

# Пример использования принципа подстановки Лисков:
battery = Battery()
drone_2 = Drone2(battery)
drone_2.gather_data()
