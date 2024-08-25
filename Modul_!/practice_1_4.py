from practice_1_5 import GPS, DistanceSensor


class Drone:
    brand = "БПЛА РФ"
    n_rotors = 4

    def __init__(self, model, weight, payload, id):
        print("Создаем экземпляр класса Drone")
        self.id = id
        self.model = model
        self.altitude = 0  # Высота в метрах
        self.speed = 0  # Скорость в метрах в секунду
        self.weight = weight  # Вес БПЛА в граммах
        self.payload = payload  # Грузоподъемность в граммах

        self.pitch = 0  # Тангаж в градусах (Поворот вокруг поперечной оси (наклон вперед или назад))
        self.roll = 0  # Крен в градусах (Поворот вокруг продольной оси (наклон влево или вправо))
        self.yaw = 0  # Рысканье в градусах (Поворот вокруг вертикальной оси)

        self.battery_capacity = 100  # Емкость батареи в процентах
        # Против часовой стрелки (CCW)
        # По часовой стрелке (CW)
        # (1)       (2)
        #  CCW      CW
        #   \        /
        #    \      /
        #     ------
        #    /      \
        #   /        \
        #  CW       CCW
        # (3)       (4)

        # int - целое
        # float - вещественное
        # str - строка
        # list - список
        self.propellers_speed = [0, 0, 0, 0]  # Скорость вращения пропеллеров в об/мин
        self.propellers_direction = ["CCW", "CW", "CW", "CCW"]  # Направление вращения пропеллеров
        # print(propellers_speed[0]) - извлечь скорость 1 пропеллера

        self.direction = 0  # Направление
        self.is_flying = False  # Летит ли БПЛА
        self.is_connected = False  # Подключен ли БПЛА
        self.is_armed = False  # Арминг двигателя
        self.speed_k = 1000  # 1 м/с = 1000 об/мин

        self.coordinates = (50.1231, 30.5231)  # начальные координаты
        self.target_coord = (30.2344, 42.5332)  # координаты цели
        self.cur_coordinates = (50.1231, 30.5231)  # начальные координаты


        self.way_coords = []  # где был дрон, его координаты пути
        self.gps = GPS(self.coordinates)
        self.dist_sensor = DistanceSensor()

    def get_dist(self):
        self.dist_sensor.get_dist()

    def get_coords(self):
        self.cur_coordinates = self.gps.update_coordinates()
        print(f"id: {self.id}, координаты: {self.cur_coordinates}")

    def __del__(self):
        print("Экземпляр класса Drone уничтожен")

    def fly(self):
        pass

    def get_info(self):
        info = f"""
        -------Квадрокоптер-------
        Бренд: {self.brand}, Модель: {self.model}
        Количество роторов: {self.n_rotors}
        Высота: {self.altitude} м, Скорость: {self.speed} м/сек.
        Вес БПЛА: {self.weight} кг, Грузоподъемность: {self.speed} гр.
        Тангаж: {self.pitch}, Крен: {self.roll} Рысканье: {self.yaw}
        Скорость вращения пропеллеров: {self.propellers_speed}
        ({self.propellers_speed[0]})       ({self.propellers_speed[1]})
         CCW      CW
          \\        /
           \\      /
            ------
           /      \\
          /        \\
         CW       CCW
        ({self.propellers_speed[2]})       ({self.propellers_speed[3]})
        """
        print(info)


if __name__ == "__main__":
    drone1 = Drone("Модель 1", 6, 1.5, "T-1000")
    drone2 = Drone("Модель 2", 3, 1.5, "T-1001")
    drone1.get_coords()
    drone1.get_coords()
    drone2.get_coords()

    drone1.get_info()
    drone2.get_info()
