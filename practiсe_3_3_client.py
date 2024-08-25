import requests  # Библиотека для выполнения HTTP-запросов
import cv2  # Библиотека для обработки изображений и видео
import time

# Базовый URL для API дрона
base_url = 'http://127.0.0.1:5000/'

# Функция для отправки телеметрических данных
def send_telemetry(latitude, longitude, altitude):
    # Формирование JSON данных с координатами и высотой
    json_data = {
        'latitude': latitude,
        'longitude': longitude,
        'altitude': altitude
    }
    # Отправка POST запроса на сервер
    response = requests.post(f"{base_url}telemetry", json=json_data)
    # Проверка наличия ответа от сервера
    if response.content:
        print(response.json())  # Вывод ответа сервера в формате JSON
    else:
        print("Пустой ответ от сервера при отправке телеметрии")

# Функция для отправки видео кадра
def send_video(video_frame):
    # Кодирование кадра в формат JPEG
    _, buffer = cv2.imencode('.jpg', video_frame)
    # Отправка POST запроса на сервер с видео данными
    response = requests.post(f"{base_url}video", data=buffer.tobytes(), headers={'Content-Type': 'application/octet-stream'})
    # Проверка статуса ответа сервера
    if response.status_code == 200:
        print("Кадр успешно отправлен")  # Успешная отправка кадра
    else:
        print("Ошибка при отправке кадра")  # Ошибка при отправке кадра

# Функция для взлета дрона
def takeoff():
    # Отправка POST запроса на сервер для взлета
    response = requests.post(f"{base_url}drone/takeoff")
    # Проверка наличия ответа от сервера
    if response.content:
        try:
            print(f"Взлет: {response.json()}")  # Вывод ответа сервера в формате JSON
        except requests.exceptions.JSONDecodeError as e:
            print(e)  # Обработка ошибки декодирования JSON
    else:
        print("Пустой ответ от сервера при взлете")

# Функция для посадки дрона
def land():
    # Отправка POST запроса на сервер для посадки
    response = requests.post(f"{base_url}drone/land")
    # Проверка наличия ответа от сервера
    if response.content:
        try:
            print(f"Посадка: {response.json()}")  # Вывод ответа сервера в формате JSON
        except requests.exceptions.JSONDecodeError as e:
            print(e)  # Обработка ошибки декодирования JSON
    else:
        print("Пустой ответ от сервера при посадке")

# Функция для обновления позиции дрона
def update_position(latitude, longitude, altitude):
    # Формирование данных для обновления позиции
    data = {
        "latitude": latitude,
        "longitude": longitude,
        "altitude": altitude
    }
    # Отправка PUT запроса на сервер для обновления позиции
    response = requests.put(f"{base_url}update_position", json=data)
    # Проверка наличия ответа от сервера
    if response.content:
        try:
            print(f"Обновление позиции: {response.json()}")  # Вывод ответа сервера в формате JSON
        except requests.exceptions.JSONDecodeError as e:
            print(e)  # Обработка ошибки декодирования JSON
    else:
        print("Пустой ответ от сервера при обновлении позиции")

# Главная функция, выполняющая основные действия
if __name__ == '__main__':
    takeoff()  # Выполнение взлета
    time.sleep(2)  # Ожидание 2 секунды

    # Обновление позиции дрона
    update_position(55.7558, 37.6176, 100)
    time.sleep(2)  # Ожидание 2 секунды
    update_position(56.1366, 40.3966, 50)
    time.sleep(2)  # Ожидание 2 секунды

    land()  # Выполнение посадки
