# класс Drone
# конструктор с атрибутами летим мы или нет и уровень заряда батереи
# взлет с проверкой батареи
# если больше 20% то разрешаем взлет (вернуть "Дрон взлетел")
# иначе (вернуть "Низкий заряд батареи для взлета")

class Drone:
    def __init__(self):
        self.is_flying = False
        self.battery_level = 100

    def takeoff(self):
        if self.battery_level > 20:
            self.is_flying = True
            return "Дрон взлетел"
        else:
            self.is_flying = False
            return "Низкий заряд батареи для взлета"

    def land(self):
        if self.is_flying:
            self.is_flying = False
            return "Дрон приземлился"
        else:
            return "Дрон уже на земле"


if __name__ == "__main__":
    drone_1 = Drone()
    print(drone_1.takeoff())