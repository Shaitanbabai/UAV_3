# Паттерн Мост
from abc import ABC, abstractmethod

# Абстрактный класс для дронов, который будет использовать различные двигатели
class Drone(ABC):
    def __init__(self, engine):
        self.engine = engine

    @abstractmethod
    def fly(self):
        pass

# Абстрактный класс для двигателей, определяет интерфейс для различных типов двигателей
class Engine(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def status(self):
        pass

    @abstractmethod
    def set_rotation_speed(self, speed: int):
        pass

# Класс для одиночного двигателя
class SingleEngine(Engine):
    def start(self):
        return "Запуск одного двигателя"

    def stop(self):
        return "Остановка одного двигателя"

    def status(self):
        return "Статус одного двигателя"

    def set_rotation_speed(self, speed: int):
        power = speed * 10  # каждый процент скорости потребляет 10 мА
        print(f"Скорость вращения одного двигателя установлена на {speed}%")
        return power  # возвращаем потребляемую мощность

# Класс для трех двигателей
class TripleEngine(Engine):
    def start(self):
        return "Запуск трех двигателей"

    def stop(self):
        return "Остановка трех двигателей"

    def status(self):
        return "Статус трех двигателей"

    def set_rotation_speed(self, speed: int):
        power = speed * 30  # каждый процент скорости потребляет 30 мА
        print(f"Скорость вращения трех двигателей установлена на {speed}%")
        return power  # возвращаем потребляемую мощность

# Класс для четырех двигателей
class QuadEngine(Engine):
    def start(self):
        return "Запуск четырех двигателей"

    def stop(self):
        return "Остановка четырех двигателей"

    def status(self):
        return "Статус четырех двигателей"

    def set_rotation_speed(self, speed: int):
        power = speed * 40  # каждый процент скорости потребляет 40 мА
        print(f"Скорость вращения четырех двигателей установлена на {speed}%")
        return power  # возвращаем потребляемую мощность

# Класс стандартного дрона, использующего двигатель
class StandartDrone(Drone):
    def fly(self):
        print(self.engine.start())
        print("Стандартный дрон в полете")
        speed = 50  # двигатель запущен на 50% мощности
        print(f"Потребляемый ток: {self.engine.set_rotation_speed(speed)} мА")
        print(self.engine.status())
        print(self.engine.stop())

# Класс продвинутого дрона, использующего двигатель
class AdvancedDrone(Drone):
    def fly(self):
        print(self.engine.start())
        print("Продвинутый дрон в полете")
        speed = 50  # двигатель запущен на 50% мощности
        print(f"Потребляемый ток: {self.engine.set_rotation_speed(speed)} мА")
        print(self.engine.status())
        print(self.engine.stop())

    def get_status(self):
        print(self.engine.status())

    def set_speed(self, speed: int):
        current = self.engine.set_rotation_speed(speed)
        print(f"Установлена скорость: {speed}%, \nПотребляемый ток: {self.engine.set_rotation_speed(speed)} мА")

if __name__ == "__main__":
    # Создаем различные типы двигателей
    single_engine = SingleEngine()
    triple_engine = TripleEngine()
    quad_engine = QuadEngine()

    # Создаем дроны с различными двигателями
    standart_drone = StandartDrone(single_engine)
    advanced_drone = AdvancedDrone(quad_engine)

    # Используем дрон
    standart_drone.fly()
    print()

    # Используем продвинутый дрон с изменением скорости
    advanced_drone.fly()
    advanced_drone.set_speed(75)
    advanced_drone.get_status()
    print()

    # Замена двигателя продвинутого дрона на трехдвигательный
    print("Замена двигателя")
    advanced_drone.engine = triple_engine
    advanced_drone.fly()
    advanced_drone.get_status()
