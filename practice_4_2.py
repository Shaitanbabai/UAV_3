from pyinstrument import Profiler
from flask import Flask, request, g, make_response
import math
import time
import random
from numba import jit
import numpy as np
import unittest

# app = Flask(__name__)

class Altimeter:
    def __init__(self, altitude=0):
        self.__altitude = altitude
        self.__rate = 0.0

    def update(self, motor_trust):
        self.__rate = motor_trust * 0.1
        self.__altitude += self.__rate + random.gauss(0, 0.1)

    def get_altitude(self):
        return self.__altitude


class Gyroscope:
    def __init__(self, orientation={'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0}):
        self.__orientation = orientation.copy()

    def update(self, roll_rate, pitch_rate, yaw_rate):
        self.__orientation['roll'] += roll_rate + random.gauss(0, 0.1)
        self.__orientation['pitch'] += pitch_rate + random.gauss(0, 0.1)
        self.__orientation['yaw'] += yaw_rate + random.gauss(0, 0.1)

    def get_orientation(self):
        return self.__orientation['roll'], self.__orientation['pitch'], self.__orientation['yaw']


class Drone:
    def __init__(self):
        self.__altimeter = Altimeter()
        self.__gyroscope = Gyroscope()
        self.__motors = [0.0, 0.0, 0.0, 0.0]
        self.__orientation = {'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0}

        self.__pid_roll = PIDRegulator(1, 0.001, 10)
        self.__pid_pitch = PIDRegulator(1, 0.001, 10)
        self.__pid_yaw = PIDRegulator(1, 0.001, 10)
        self.__pid_altitude = PIDRegulator(1, 0.001, 10)

    def get_altitude(self):
        # получим с датчиков
        return self.__altimeter.get_altitude()

    def update_altitude(self):
        self.__altitude = self.get_altitude()
        self.__orientation['roll'], self.__orientation['pitch'], self.__orientation['yaw'] = self.get_gyroscope()

    def get_gyroscope(self):
        # получим с датчиков
        self.__gyroscope.update(self.__orientation['roll'], self.__orientation['pitch'], self.__orientation['yaw'])
        self.__orientation = self.__gyroscope.get_orientation()
        return self.__orientation['roll'], self.__orientation['pitch'], self.__orientation['yaw']

    def motor_trust(self, trusts):
        self.__motors = trusts
        average_trust = sum(trusts) / len(trusts)

        self.__altimeter.update(average_trust)
        # Против часовой стрелки (CCW)
        # По часовой стрелке (CW)
        # (0)       (1)
        #  CCW      CW
        #   \        /
        #    \      /
        #     ------
        #    /      \
        #   /        \
        #  CW       CCW
        # (2)       (3)
        yaw_rate = (self.__motors[0] - self.__motors[1] - self.__motors[2] + self.__motors[3]) / 4
        pitch_rate = (self.__motors[0] + self.__motors[1] - self.__motors[2] - self.__motors[3]) / 4
        roll_rate = (self.__motors[0] - self.__motors[1] + self.__motors[2] - self.__motors[3]) / 4

        self.__gyroscope.update(roll_rate, pitch_rate, yaw_rate)
        print(f"Тяга: {trusts}, Альтиметр: {self.__altimeter.get_altitude()}, Гироскоп: {self.__gyroscope.get_orientation()}")

    def control(self, target_altitude, target_orientation):
        self.update_altitude()
        self.get_gyroscope()

        altitude_output, _, _ = self.__pid_altitude.update(target_altitude, self.__altitude)

        roll_output, _, _ = self.__pid_altitude.update(target_orientation["roll"], self.__orientation["roll"])
        pitch_output, _, _ = self.__pid_altitude.update(target_orientation["pitch"], self.__orientation["pitch"])
        yaw_output, _, _ = self.__pid_altitude.update(target_orientation["yaw"], self.__orientation["yaw"])

        trusts = [
            altitude_output + roll_output + pitch_output + yaw_output,
            altitude_output - roll_output + pitch_output - yaw_output,
            altitude_output + roll_output - pitch_output - yaw_output,
            altitude_output - roll_output - pitch_output + yaw_output,
        ]

        self.motor_trust(trusts)



class PIDRegulator:
    def __init__(self, kp, ki, kd):
        self.__kp = kp
        self.__ki = ki
        self.__kd = kd
        self.old_error = 0.0
        self.integral_error = 0.0

    def update(self, setpoint, pv):
        error = setpoint - pv
        self.integral_error += error
        derivative_error = error - self.old_error
        self.old_error = error
        u = (self.__kp * error) + (self.__ki * self.integral_error) + (self.__kd * derivative_error)
        return u, error, self.integral_error



# def pid_regulator():

def get_sensor_data():
    time.sleep(0.05)
    return {
        "altitude": random.randint(0, 500),
        "speed": random.randint(0, 70)
    }

def process(data):
    time.sleep(0.1)
    return {
        "altitude": data["altitude"] / 39.37,   # перевод дюймов в метры
        "speed": data["speed"] * 0.609          # перевод милли/час в км/час
    }

def make_decision(data):
    time.sleep(0.2)
    if data["altitude"] < 50:
        return "Подниматься выше"
    return "Опускайся ниже"

def motor_control(decision):
    time.sleep(0.2)
    return f"Задача мотора: {decision}"

# @app.route('/')
# def index():
#     data = get_sensor_data()
#     process_data = process(data)
#     decision = make_decision(process_data)
#     motor = motor_control(decision)
#
#     return f'Управление дроном\n{motor}'
#
#
# @app.before_request
# def before_request():
#     g.is_profiling = "profile" in request.args
#     if g.is_profiling:
#         g.profile = Profiler()
#         g.profile.start()
#
#
# @app.after_request
# def after_request(response):
#     if g.is_profiling:
#         g.profile.stop()
#         output_html = g.profile.output_html()
#         return make_response(output_html)
#     return response


# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == "__main__":
    drone = Drone()
    target_altitude = 10.0  # Задаем целевую высоту в 10 метров
    target_orientation = {'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0}  # Ориентация остается нейтральной

    # Запуск симуляции на 100 итераций
    for _ in range(100):
        drone.control(target_altitude, target_orientation)