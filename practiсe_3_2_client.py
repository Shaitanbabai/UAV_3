import requests  # Импорт библиотеки для выполнения HTTP-запросов
import cv2  # Импорт библиотеки для обработки изображений и видео
import time  # Импорт библиотеки для работы с временем

# Базовый URL для API сервера дрона
base_url = 'http://127.0.0.1:5000/'


# Функция для отправки телеметрических данных на сервер
def send_telemetry(latitude, longitude, altitude):
    # Формирование JSON данных с координатами и высотой
    json_data = {
        'latitude': latitude,
        'longitude': longitude,
        'altitude': altitude
    }
    # Отправка POST запроса на сервер с телеметрическими данными
    response = requests.post(f"{base_url}telemetry", json=json_data)
    # Печать ответа сервера в формате JSON
    print(response.json())


# Функция для отправки видео кадра на сервер
def send_video(video_frame):
    # Кодирование кадра в формат JPEG
    _, buffer = cv2.imencode('.jpg', video_frame)
    # Отправка POST запроса на сервер с видео данными
    response = requests.post(f"{base_url}video", data=buffer.tobytes())
    # Проверка статуса ответа сервера
    if response.status_code == 204:
        print("Кадр успешно отправлен")  # Успешная отправка кадра
    else:
        print("Ошибка при отправке кадра")  # Ошибка при отправке кадра


# Главная функция
if __name__ == '__main__':
    # Отправка телеметрических данных
    send_telemetry(55.5555, 37.7777, 100.0)

    # Инициализация захвата видео с веб-камеры
    cap = cv2.VideoCapture(0)

    # Установка частоты кадров
    fps = 60

    # Цикл для захвата и отправки видео кадров
    while cap.isOpened():
        ret, frame = cap.read()  # Захват кадра
        if not ret:
            break  # Прерывание цикла, если кадр не захвачен
        send_video(frame)  # Отправка видео кадра на сервер
        time.sleep(1 / fps)  # Задержка для достижения нужного fps

    # Освобождение захвата видео и уничтожение всех окон OpenCV
    cap.release()
    cv2.destroyAllWindows()
