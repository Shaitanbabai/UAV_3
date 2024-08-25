from pymavlink import mavutil

# Класс для управления дроном
class Drone:
    def __init__(self, connect_uri):
        # Инициализация соединения с дроном через MAVLink
        self.master = mavutil.mavlink_connection(connect_uri)
        # Ожидание сигнала от дрона (heartbeat), чтобы убедиться, что соединение установлено
        self.master.wait_heartbeat()
        print("Соединение с дроном установлено")

    # Метод для армирования дрона (разблокировки двигателей)
    def arm(self):
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,  # Команда на армирование/разармирование
            0,
            1, 0, 0, 0, 0, 0, 0  # Армирование (1 - армировать, 0 - разармировать)
        )
        print("Армирование дрона завершено")

    # Метод для разармирования дрона (блокировки двигателей)
    def disarm(self):
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,  # Команда на армирование/разармирование
            0,
            0, 0, 0, 0, 0, 0, 0  # Разармирование (1 - армировать, 0 - разармировать)
        )
        print("Двигатели дрона заблокированы")

    # Метод для взлета дрона на заданную высоту
    def takeoff(self, altitude):
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,  # Команда на взлет
            0,
            0, 0, 0, 0, 0, 0, altitude  # Задание высоты взлета
        )
        print(f"Взлет на высоту {altitude} м")

    # Метод для полета дрона к заданной точке (широта, долгота, высота)
    def fly_to(self, latitude, longitude, altitude):
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            0,
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,  # Рамка для координат относительно заданной высоты
            mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,  # Команда на полет к точке
            0, 0,
            0, 0, 0,
            latitude, longitude, altitude  # Задание координат (широта, долгота, высота)
        )
        print(f"Летим к точке: {latitude, longitude, altitude}")

    # Метод для посадки дрона
    def land(self):
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_NAV_LAND,  # Команда на посадку
            0,
            0, 0, 0, 0, 0, 0, 0  # Посадка с текущей позиции
        )
        print(f"Дрон приземлился")

# Основной блок кода для выполнения команд
if __name__ == '__main__':
    drone_1 = Drone("udp:127.0.0.1:14550")  # Создание экземпляра класса Drone и подключение к дрону
    drone_1.arm()  # Армирование дрона
    drone_1.takeoff(10)  # Взлет на высоту 10 метров
    latitude, longitude, altitude = 40.4444, 50.5555, 10  # Задание координат для полета
    drone_1.fly_to(latitude, longitude, altitude)  # Полет к заданной точке
    drone_1.land()  # Посадка дрона
    drone_1.disarm()  # Разармирование дрона
