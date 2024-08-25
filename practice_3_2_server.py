from flask import Flask, Response, request, jsonify  # Импорт необходимых модулей Flask
import cv2  # Импорт библиотеки OpenCV для обработки изображений
import numpy as np  # Импорт библиотеки NumPy для работы с массивами
import time

# Инициализация Flask-приложения
app = Flask(__name__)

# Инициализация состояния дрона
drone_state = {
    "status": "landed",  # Текущий статус дрона: "landed" или "flying"
    "position": {  # Текущая позиция дрона
        "latitude":  0.0,  # Широта
        "longitude": 0.0,  # Долгота
        "altitude":  0.0   # Высота
    },
    "telemetry_data": []  # Список для хранения телеметрических данных
}

# Переменная для хранения текущего видео кадра
video_frame = None

# Частота кадров (кадров в секунду)
fps = 10

# Качество видео (в процентах)
quality = 80

# Маршрут для взлета дрона
@app.route("/drone/takeoff", methods=["POST"])
def takeoff():
    try:
        # Проверка, не находится ли дрон уже в воздухе
        if drone_state["status"] == "flying":
            return jsonify({"error": "Дрон уже в воздухе"}), 400

        # Обновление статуса и высоты дрона
        drone_state["status"] = "flying"
        drone_state["position"]["altitude"] = 10.0

        app.logger.info("Дрон взлетел")
        return jsonify({
            "message": "Взлет выполнен",
            "drone_state": drone_state
        }), 200
    except Exception as e:
        app.logger.error(f"Ошибка при взлете: {e}")
        return jsonify({"error": "Ошибка при взлете"}), 500

# Маршрут для приема телеметрических данных
@app.route("/telemetry", methods=["POST"])
def receive_telemetry():
    data = request.json  # Получение данных из запроса
    drone_state["telemetry_data"].append(data)  # Добавление данных в список телеметрии
    return jsonify({"status": "Получили"}), 200

# Маршрут для отображения всех телеметрических данных
@app.route("/display", methods=["GET"])
def display_telemetry():
    return jsonify(drone_state["telemetry_data"]), 200  # Возвращение всех телеметрических данных

# Маршрут для приема видео кадра
@app.route("/video", methods=["POST"])
def receive_video():
    global video_frame  # Использование глобальной переменной для хранения видео кадра
    np_array = np.frombuffer(request.data, dtype=np.uint8)  # Преобразование данных запроса в numpy массив
    video_frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)  # Декодирование массива в изображение
    return "", 204  # Возвращение пустого ответа с кодом 204 (No Content)

# Маршрут для трансляции видео потока
@app.route("/video_feed")
def video_feed():
    def generate():
        global video_frame  # Использование глобальной переменной для хранения видео кадра
        while True:
            if video_frame is not None:
                # Кодирование изображения в формат JPEG
                _, buffer = cv2.imencode('.jpg', video_frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
                frame = buffer.tobytes()  # Преобразование буфера в байты
                # Генерация потока кадра
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(1 / fps)  # Задержка для достижения нужного fps
    # Возвращение ответа с типом MIME multipart/x-mixed-replace и границей frame
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Запуск Flask-приложения
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
