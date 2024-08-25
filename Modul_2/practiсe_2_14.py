from abc import ABC, abstractmethod


class DroneRepository(ABC):
    @abstractmethod
    def get_all_drones(self):
        """Получить список всех дронов"""
        pass

    @abstractmethod
    def get_drone_by_id(self, id: int):
        pass

    @abstractmethod
    def update_drone_status(self, id: int, status: str):
        """Обнявляем статус дрона по id (ожидание, в полете, зарядка)"""
        pass

    @abstractmethod
    def add_drone(self, drone: dict):
        pass

    @abstractmethod
    def remove_drone(self, id: int):
        pass


class MemoryDroneRepository(DroneRepository):
    def __init__(self):
        self._drones = {}

    def get_all_drones(self):
        """Получить список всех дронов в памяти"""
        return list(self._drones.values())

    def get_drone_by_id(self, id: int):
        return self._drones.get(id, None)

    def update_drone_status(self, id: int, status: str):
        if id in self._drones:
            self._drones[id]['status'] = status

    def add_drone(self, drone: dict):
        id = drone['id']
        self._drones[id] = drone

    def remove_drone(self, id: int):
        del self._drones[id]


def list_all_drones(drone_repository: DroneRepository):
    drones = drone_repository.get_all_drones()
    for drone in drones:
        print(f"Дрон id: {drone['id']}, status: {drone['status']}")

if __name__ == '__main__':
    drone_repository = MemoryDroneRepository()
    drone_1 = {"id": 1, "status": "idle"}
    drone_2 = {"id": 2, "status": "flying"}
    drone_repository.add_drone(drone_1)
    drone_repository.add_drone(drone_2)
    list_all_drones(drone_repository)
    drone_repository.update_drone_status(1, "charge")
    print("--------------")

    list_all_drones(drone_repository)
    drone_repository.remove_drone(2)

    print("--------------")
    list_all_drones(drone_repository)
