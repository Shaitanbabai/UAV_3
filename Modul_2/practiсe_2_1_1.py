# Фабричный метод

from abc import ABC, abstractmethod

# Абстрактный класс для миссий, определяющий интерфейс выполнения миссии
class Mission(ABC):
    @abstractmethod
    def execute(self):
        pass

# Конкретные классы миссий, наследующие от абстрактного класса Mission
class BackMission(Mission):
    def execute(self):
        return "Выполнение миссии: возврат на базу"

class MappingMission(Mission):
    def execute(self):
        return "Выполнение миссии: картографирование"

class PatrolMission(Mission):
    def execute(self):
        return "Выполнение миссии: патрулирование"

class FireFightingMission(Mission):
    def execute(self):
        return "Выполнение миссии: тушение пожара"

class EvacuationMission(Mission):
    def execute(self):
        return "Выполнение миссии: эвакуация"

class FollowingMission(Mission):
    def execute(self):
        return "Выполнение миссии: следование за объектом"

# Абстрактный класс фабрики миссий, определяющий интерфейс создания миссий
class MissionFactory(ABC):
    @abstractmethod
    def create_mission(self):
        pass

# Конкретные фабрики для создания определенных миссий
class BackMissionFactory(MissionFactory):
    def create_mission(self):
        return BackMission()

class MappingMissionFactory(MissionFactory):
    def create_mission(self):
        return MappingMission()

class PatrolMissionFactory(MissionFactory):
    def create_mission(self):
        return PatrolMission()

class FireFightingMissionFactory(MissionFactory):
    def create_mission(self):
        return FireFightingMission()

class EvacuationMissionFactory(MissionFactory):
    def create_mission(self):
        return EvacuationMission()

class FollowingMissionFactory(MissionFactory):
    def create_mission(self):
        return FollowingMission()

# Функция планирования миссий, принимает фабрику и выполняет созданную миссию
def mission_planner(factory: MissionFactory):
    mission = factory.create_mission()
    return mission.execute()

# Пример использования фабричных методов для создания и выполнения миссий
patrol_factory = PatrolMissionFactory()
print(mission_planner(patrol_factory))  # Вывод: "Выполнение миссии: патрулирование"

mapping_factory = MappingMissionFactory()
print(mission_planner(mapping_factory))  # Вывод: "Выполнение миссии: картографирование"
