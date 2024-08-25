from abc import ABC, abstractmethod

# Интерфейс для дрона
class DroneInterface(ABC):
    @abstractmethod
    def take_off(self):
        pass

# Реальный объект - Дрон
class Drone(DroneInterface):
    def take_off(self):
        print("Дрон взлетает.")

# Прокси-класс для обеспечения безопасности
class SecureDroneProxy(DroneInterface):
    def __init__(self, drone, user):
        self.drone = drone
        self.user = user

    def take_off(self):
        # Проверка прав пользователя перед взлетом дрона
        if self.user.has_permission("take_off"):
            self.drone.take_off()
        else:
            print(f"Доступ для {self.user.nick} запрещен: Взлет невозможен.")

# Класс пользователя
class User:
    def __init__(self, nick, permissions):
        self.permissions = permissions
        self.nick = nick

    def has_permission(self, permission):
        # Проверка наличия у пользователя необходимого разрешения
        return permission in self.permissions

# Пример использования
drone = Drone()

# Пользователь с правами на взлет
user_with_access = User(nick="Admin", permissions=["take_off"])
secure_drone_proxy = SecureDroneProxy(drone, user_with_access)
secure_drone_proxy.take_off()  # Вывод: Дрон взлетает.

# Пользователь без прав на взлет
user_without_access = User(nick="Guest", permissions=[])
secure_drone_proxy_no_access = SecureDroneProxy(drone, user_without_access)
secure_drone_proxy_no_access.take_off()  # Вывод: Доступ запрещен: Взлет невозможен
