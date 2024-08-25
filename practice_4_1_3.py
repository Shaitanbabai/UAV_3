from pyinstrument import Profiler
from flask import Flask, request, g, make_response
import math
import time
import random

app = Flask(__name__)

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

@app.route('/')
def index():
    data = get_sensor_data()
    process_data = process(data)
    decision = make_decision(process_data)
    motor = motor_control(decision)

    return f'Управление дроном\n{motor}'


@app.before_request
def before_request():
    g.is_profiling = "profile" in request.args
    if g.is_profiling:
        g.profile = Profiler()
        g.profile.start()


@app.after_request
def after_request(response):
    if g.is_profiling:
        g.profile.stop()
        output_html = g.profile.output_html()
        return make_response(output_html)
    return response


if __name__ == '__main__':
    app.run(debug=True)
