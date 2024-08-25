# Паттерн Команда и Стратегия
from abc import ABC, abstractmethod

# Класс для управления дроном, включает методы для выполнения основных команд
class DroneController:
    """
    Класс для управления дроном. Содержит методы для взлета, движения вперед и поворотов.
    """

    def takeoff(self):
        """
        Команда для взлета дрона.
        """
        print('Дрон взлетает...')

    def move_forward(self, distance: float):
        """
        Команда для движения вперед на заданное расстояние.
        :param distance: Расстояние, на которое дрон должен пролететь вперед.
        """
        print(f"Летим вперед на {distance} метров")

    def turn(self, degree: float):
        """
        Команда для поворота дрона на заданное количество градусов.
        :param degree: Угол поворота в градусах.
        """
        print(f"Поворачиваем на {degree} градусов")

# Интерфейс команды, определяет метод execute
class ICommand(ABC):
    @abstractmethod
    def execute(self):
        """
        Метод для выполнения команды.
        """
        pass

    # Метод для отмены команды (раскомментируйте для использования)
    # def undo(self):
    #     pass

# Команда для взлета дрона
class Takeoff(ICommand):
    def __init__(self, drone: DroneController):
        self.__drone = drone  # Хранит ссылку на объект DroneController

    def execute(self):
        # Выполняет команду взлета
        self.__drone.takeoff()

# Команда для движения дрона вперед
class MoveForward(ICommand):
    def __init__(self, drone: DroneController, distance: float):
        self.__drone = drone  # Хранит ссылку на объект DroneController
        self.__distance = distance  # Расстояние для движения вперед

    def execute(self):
        # Выполняет команду движения вперед на заданное расстояние
        self.__drone.move_forward(self.__distance)

# Команда для поворота дрона
class Turn(ICommand):
    def __init__(self, drone: DroneController, degree: float):
        self.__drone = drone  # Хранит ссылку на объект DroneController
        self.__degree = degree  # Угол поворота

    def execute(self):
        # Выполняет команду поворота на заданный угол
        self.__drone.turn(self.__degree)

# Интерфейс стратегии полета, определяет метод execute
class IFlightStrategy(ABC):
    @abstractmethod
    def execute(self, commands: list):
        """
        Метод для выполнения списка команд в рамках стратегии.
        :param commands: Список команд для выполнения.
        """
        pass

# Стратегия разведывательной миссии
class ReconMissionStrategy(IFlightStrategy):
    def execute(self, commands: list):
        # Выполняет разведывательную миссию, выполняя все команды в списке
        print(f"Начало выполнения разведывательной миссии")
        for command in commands:
            command.execute()
        print(f"Конец миссии")

# Стратегия патрульной миссии
class PatrolMissionStrategy(IFlightStrategy):
    def __init__(self, n_patrols: int):
        self.__n_patrols = n_patrols  # Количество циклов патрулирования

    def execute(self, commands: list):
        # Выполняет патрульную миссию, повторяя все команды в списке заданное количество раз
        print(f"Начало выполнения миссии патрулирования")
        for _ in range(self.__n_patrols):
            for command in commands:
                command.execute()
            print("Патрулирование выполнено")
        print(f"Конец миссии")

# Контекст для управления стратегиями полета дрона
class DroneContext:
    def __init__(self, strategy: IFlightStrategy = None):
        self.__strategy = strategy  # Текущая стратегия полета
        self.__commands = []  # Список команд

    def set_strategy(self, strategy: IFlightStrategy):
        """
        Устанавливает стратегию полета.
        :param strategy: Объект, реализующий интерфейс IFlightStrategy.
        """
        self.__strategy = strategy

    def add_command(self, command: ICommand):
        """
        Добавляет команду в список для выполнения.
        :param command: Объект, реализующий интерфейс ICommand.
        """
        self.__commands.append(command)

    def execute(self):
        """
        Выполняет все команды, используя текущую стратегию полета.
        После выполнения команды очищает список.
        """
        self.__strategy.execute(self.__commands)
        self.__commands.clear()


