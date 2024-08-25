# Паттерн Команда

from abc import ABC, abstractmethod


# Абстрактный класс для команд
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


# Класс, представляющий дрон с возможностью выполнять различные операции
class Drone:
    def take_off(self):
        print("БПЛА взлетает")

    def land(self):
        print("БПЛА приземляется")

    def change_course(self, new_course):
        print(f"Дрон меняет курс на {new_course}")


# Команда на взлет
class TakeOFF(Command):
    def __init__(self, drone: Drone):
        self._drone = drone

    def execute(self):
        self._drone.take_off()

    def undo(self):
        self._drone.land()


# Команда на посадку
class Land(Command):
    def __init__(self, drone: Drone):
        self._drone = drone

    def execute(self):
        self._drone.land()

    def undo(self):
        print("Отмена посадки невозможна")


# Команда на изменение курса
class ChangeCourse(Command):
    def __init__(self, drone: Drone, course):
        self._drone = drone
        self._course = course
        self._previous_course = None

    def execute(self):
        self._previous_course = "предыдущий курс"
        self._drone.change_course(self._course)

    def undo(self):
        if self._previous_course:
            self._drone.change_course(self._previous_course)


# Класс для управления командами
class RemoteControl:
    def __init__(self):
        self._commands = []  # Список команд для выполнения
        self._history = []  # История выполненных команд

    def add_command(self, command: Command):
        self._commands.append(command)

    def execute_command(self):
        # Выполнение всех команд из списка
        for command in self._commands:
            command.execute()
            self._history.append(command)

