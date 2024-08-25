from flask import Flask, Response, request, jsonify
import cv2
import numpy as np
import time

# Инициализация Flask-приложения
app = Flask(__name__)

# Инициализация состояния дрона
drone_state = {
    "status": "landed",  # Текущий статус дрона: взлетел или на земле
    "position": {  # Текущая позиция дрона
        "latitude": 0.0,
        "longitude": 0.0,
        "altitude": 0.0
    },
    "telemetry_data": []  # Список для хранения телеметрических данных
}

# Переменная для хранения текущего видео кадра
video_frame = None
# Частота кадров видео (fps)
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

        # Обновление статуса и позиции дрона
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

# Маршрут для посадки дрона
@app.route("/drone/land", methods=["POST"])
def land():
    try:
        # Проверка, не находится ли дрон уже на земле
        if drone_state["status"] == "landed":
            return jsonify({"error": "Дрон уже на земле"}), 400

        # Обновление статуса и позиции дрона
        drone_state["status"] = "landed"
        drone_state["position"]["altitude"] = 0.0

        app.logger.info("Дрон приземлился")
        return jsonify({
            "message": "Посадка выполнена",
            "drone_state": drone_state
        }), 200
    except Exception as e:
        app.logger.error(f"Ошибка при посадке: {e}")
        return jsonify({"error": "Ошибка при посадке"}), 500

# Маршрут для обновления позиции дрона
@app.route("/update_position", methods=["PUT"])
def update_position():
    data = request.json
    app.logger.info(f"Полученные данные для обновления позиции: {data}")

    # Проверка наличия данных
    if not data:
        app.logger.error("Пустые данные")
        return jsonify({"error": "Ошибка в данных"}), 400

    # Обновление позиции дрона
    drone_state["position"]["latitude"] = float(data["latitude"])
    drone_state["position"]["longitude"] = float(data["longitude"])
    drone_state["position"]["altitude"] = float(data["altitude"])

    response = {
        "message": "Позиция обновлена",
        "drone_state": drone_state
    }
    app.logger.info(f"Ответ на обновление позиции: {response}")

    return jsonify(response), 200

# Маршрут для приема телеметрических данных
@app.route("/telemetry", methods=["POST"])
def receive_telemetry():
    data = request.json
    # Добавление новых телеметрических данных в список
    drone_state["telemetry_data"].append(data)
    return jsonify({"status": "Получили"}), 200

# Маршрут для отображения всех телеметрических данных
@app.route("/display", methods=["GET"])
def display_telemetry():
    return jsonify(drone_state["telemetry_data"]), 200

# Маршрут для приема видео кадра
@app.route("/video", methods=["POST"])
def receive_video():
    global video_frame
    # Преобразование данных из запроса в numpy массив
    np_array = np.frombuffer(request.data, dtype=np.uint8)
    # Декодирование массива в изображение
    video_frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    if video_frame is None:
        return jsonify({"error": "Ошибка декодирования кадра"}), 400
    return jsonify({"status": "Кадр получен"}), 200

# Маршрут для трансляции видео потока
@app.route("/video_feed")
def video_feed():
    def generate():
        global video_frame
        while True:
            if video_frame is not None:
                # Кодирование изображения в формат JPEG
                _, buffer = cv2.imencode('.jpg', video_frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
                frame = buffer.tobytes()
                # Генерация потока кадра
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            # Задержка для достижения нужного fps
            time.sleep(1 / fps)

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Запуск Flask-приложения
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
