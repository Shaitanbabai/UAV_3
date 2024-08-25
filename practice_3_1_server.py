from flask import Flask, request, jsonify  # Импорт необходимых модулей Flask
import logging  # Импорт модуля для логирования

# Инициализация Flask-приложения
app = Flask(__name__)

# Настройка логирования для приложения
logging.basicConfig(level=logging.INFO)

# Инициализация состояния дрона
drone_state = {
    "status": "landed",  # Текущий статус дрона: "landed" или "flying"
    "position": {  # Текущая позиция дрона
        "latitude":  0.0,  # Широта
        "longitude": 0.0,  # Долгота
        "altitude":  0.0   # Высота
    }
}

# Маршрут для взлета дрона
@app.route("/drone/takeoff", methods=["POST"])
def takeoff():
    try:
        # Проверка, не находится ли дрон уже в воздухе
        if drone_state["status"] == "flying":
            return jsonify({"error": "Дрон уже в воздухе"}), 400  # Возврат ошибки, если дрон уже в воздухе

        # Обновление статуса и высоты дрона
        drone_state["status"] = "flying"
        drone_state["position"]["altitude"] = 10.0

        app.logger.info("Дрон взлетел")  # Логирование успешного взлета
        return jsonify({
            "message": "Взлет выполнен",
            "drone_state": drone_state
        }), 200  # Возврат успешного ответа с обновленным состоянием дрона
    except Exception as e:
        app.logger.error(f"Ошибка при взлете: {e}")  # Логирование ошибки при взлете
        return jsonify({"error": "Ошибка при взлете"}), 500  # Возврат ошибки сервера

# Главная функция, запускающая Flask-приложение
if __name__ == '__main__':
    app.run(debug=True)  # Запуск Flask-приложения с включенным режимом отладки
