from pyinstrument import Profiler
from flask import Flask, request, g, make_response, jsonify
import random
import time

app = Flask(__name__)

class Altimeter:
    def __init__(self, altitude=0):
        self.__altitude = altitude
        self.__rate = 0.0

    def update(self, motor_trust):
        # Обновляем скорость изменения высоты в зависимости от тяги моторов
        self.__rate = motor_trust * 0.1
        # Изменяем текущую высоту с добавлением случайного шума
        self.__altitude += self.__rate + random.gauss(0, 0.1)

    def get_altitude(self):
        # Возвращаем текущую высоту с округлением до 4 знаков после запятой
        return round(self.__altitude, 4)


class Gyroscope:
    def __init__(self, orientation=None):
        # Начальные значения ориентации
        if orientation is None:
            orientation = {'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0}
        self.__orientation = orientation.copy()

    def update(self, roll_rate, pitch_rate, yaw_rate):
        # Обновляем значения ориентации с добавлением случайного шума и округлением до 4 знаков после запятой
        self.__orientation['roll'] += round(roll_rate + random.gauss(0, 0.1), 4)
        self.__orientation['pitch'] += round(pitch_rate + random.gauss(0, 0.1), 4)
        self.__orientation['yaw'] += round(yaw_rate + random.gauss(0, 0.1), 4)

    def get_orientation(self):
        # Возвращаем текущую ориентацию
        return self.__orientation


class Drone:
    def __init__(self):
        self.__altimeter = Altimeter()
        self.__gyroscope = Gyroscope()
        self.__motors = [0.0, 0.0, 0.0, 0.0]
        self.__orientation = {'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0}

        # Настройки PID-регуляторов для управления дроном
        self.__pid_roll = PIDRegulator(1, 0.0001, 0.05)
        self.__pid_pitch = PIDRegulator(1, 0.0001, 0.05)
        self.__pid_yaw = PIDRegulator(1, 0.0001, 0.05)
        self.__pid_altitude = PIDRegulator(1, 0.0001, 0.05)

        # Ограничения значений ориентации
        self.max_orientation_value = 45.0  # Максимальный угол в градусах

    def get_altitude(self):
        # Получаем текущую высоту
        return self.__altimeter.get_altitude()

    def update_altitude(self):
        # Обновляем данные о высоте и ориентации
        self.__altitude = self.get_altitude()
        self.__orientation = self.get_gyroscope()
        # Выводим текущую высоту в консоль с точностью до 4 знаков после запятой
        print(f"Текущая высота: {self.__altitude:.4f} м")

    def get_gyroscope(self):
        # Обновляем ориентацию
        self.__gyroscope.update(self.__orientation['roll'], self.__orientation['pitch'], self.__orientation['yaw'])
        self.__orientation = self.__gyroscope.get_orientation()

        # Ограничиваем значения ориентации по максимальному углу
        self.__orientation['roll'] = max(min(self.__orientation['roll'], self.max_orientation_value), -self.max_orientation_value)
        self.__orientation['pitch'] = max(min(self.__orientation['pitch'], self.max_orientation_value), -self.max_orientation_value)
        self.__orientation['yaw'] = max(min(self.__orientation['yaw'], self.max_orientation_value), -self.max_orientation_value)

        return self.__orientation

    def motor_trust(self, trusts):
        # Устанавливаем значения тяги моторов
        self.__motors = trusts
        average_trust = sum(trusts) / len(trusts)
        # Обновляем высоту на основе средней тяги моторов
        self.__altimeter.update(average_trust)

        # Расчет скоростей изменения ориентации (углов)
        yaw_rate = (self.__motors[0] - self.__motors[1] - self.__motors[2] + self.__motors[3]) / 4
        pitch_rate = (self.__motors[0] + self.__motors[1] - self.__motors[2] - self.__motors[3]) / 4
        roll_rate = (self.__motors[0] - self.__motors[1] + self.__motors[2] - self.__motors[3]) / 4

        # Округляем скорости до 4 знаков после запятой
        yaw_rate = round(yaw_rate, 4)
        pitch_rate = round(pitch_rate, 4)
        roll_rate = round(roll_rate, 4)

        # Обновляем данные гироскопа
        self.__gyroscope.update(roll_rate, pitch_rate, yaw_rate)

        # Выводим текущие параметры в консоль с округлением значений тяги и ориентации
        print(f"Тяга: {[round(trust, 4) for trust in trusts]}, Альтиметр: {self.__altimeter.get_altitude()}, Гироскоп: {self.__gyroscope.get_orientation()}")

    def control(self, target_altitude, target_orientation):
        # Управляем дроном на основе заданной высоты и ориентации
        self.update_altitude()
        self.get_gyroscope()

        # Вычисляем управляющие воздействия с помощью PID-регуляторов
        altitude_output, _, _ = self.__pid_altitude.update(target_altitude, self.__altitude)
        roll_output, _, _ = self.__pid_roll.update(target_orientation["roll"], self.__orientation["roll"])
        pitch_output, _, _ = self.__pid_pitch.update(target_orientation["pitch"], self.__orientation["pitch"])
        yaw_output, _, _ = self.__pid_yaw.update(target_orientation["yaw"], self.__orientation["yaw"])

        # Распределяем тягу между моторами
        trusts = [
            altitude_output + roll_output + pitch_output + yaw_output,
            altitude_output - roll_output + pitch_output - yaw_output,
            altitude_output + roll_output - pitch_output - yaw_output,
            altitude_output - roll_output - pitch_output + yaw_output,
        ]

        # Обновляем тягу моторов
        self.motor_trust(trusts)

    def get_coordinates(self):
        # Возвращаем текущие координаты дрона: высоту и ориентацию
        return {
            "altitude": round(self.get_altitude(), 4),
            "orientation": {k: round(v, 4) for k, v in self.get_gyroscope().items()}
        }


class PIDRegulator:
    def __init__(self, kp, ki, kd):
        # Инициализация коэффициентов PID-регулятора
        self.__kp = kp
        self.__ki = ki
        self.__kd = kd
        self.old_error = 0.0
        self.integral_error = 0.0

    def update(self, setpoint, pv):
        # Расчет управляющего воздействия на основе текущей ошибки, интегральной и производной
        error = setpoint - pv
        self.integral_error += error
        derivative_error = error - self.old_error
        self.old_error = error
        u = (self.__kp * error) + (self.__ki * self.integral_error) + (self.__kd * derivative_error)
        return u, error, self.integral_error


@app.route('/')
def index():
    # Обновление состояния дрона перед отправкой ответа
    drone.control(target_altitude, target_orientation)

    coordinates = drone.get_coordinates()
    # Возвращаем данные в формате JSON
    return jsonify({
        "altitude": coordinates["altitude"],
        "orientation": coordinates["orientation"]
    })

@app.before_request
def before_request():
    # Проверяем, нужно ли профилировать запрос
    g.is_profiling = "profile" in request.args
    if g.is_profiling:
        g.profile = Profiler()
        g.profile.start()


@app.after_request
def after_request(response):
    # Останавливаем профилирование и выводим отчет, если это было запрошено
    if g.is_profiling:
        g.profile.stop()
        output_html = g.profile.output_html()
        return make_response(output_html)
    return response


if __name__ == '__main__':
    drone = Drone()
    target_altitude = 10.0  # Задаем целевую высоту в 10 метров
    target_orientation = {'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0}  # Ориентация остается нейтральной

    app.run(debug=True)
