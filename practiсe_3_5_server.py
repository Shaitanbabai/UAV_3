import requests
from flask import Flask, Response, request, jsonify

# Управление дронами

# GET
# /drones - Получить список всех дронов
# /drones/{drone_id} - Получить информацию о конкретном дроне

# POST
# /drones - Создать нового дрона

# PUT
# /drones/{drone_id} - Обновить информацию о конкретном дроне

# DELETE
# /drones/{drone_id} - Удалить конкретного дрона


# Управление полетом

# POST
# /drones/{drone_id}/takeoff - Команда взлета дрона
# /drones/{drone_id}/land - Команда посадки дрона
# /drones/{drone_id}/move - Команда перемещения дрона

# GET
# /drones/{drone_id}/sensors - Получить данные сенсоров дрона

# Пример взлета
# POST /drones/{drone_id}/takeoff
# {
#     "altitude": 10
# }

# Создаем экземпляр Flask приложения
app = Flask(__name__)

# Инициализируем словарь для хранения информации о дронах
drones = {}

@app.route("/drones", methods=["GET"])
def get_drones():
    """
    Возвращает список всех дронов.

    :return: JSON-ответ со списком всех дронов и статус-код 200
    """
    return jsonify(drones), 200

@app.route("/drones/<drone_id>", methods=["GET"])
def get_drone(drone_id):
    """
    Возвращает информацию о конкретном дроне.

    :param drone_id: идентификатор дрона
    :return: JSON-ответ с информацией о дроне и статус-код 200,
             или ошибка 404, если дрон не найден
    """
    drone = drones.get(drone_id)
    if drone:
        return jsonify(drone), 200
    return jsonify({"error": "Дрон не найден"}), 404

@app.route("/drones", methods=["POST"])
def create_drone():
    """
    Создает нового дрона.

    :return: JSON-ответ с сообщением об успешном добавлении дрона и статус-код 201,
             или ошибка 404, если не передан id дрона
    """
    drone_id = request.json.get("drone_id")
    if drone_id:
        drones[drone_id] = request.json
        return jsonify({"message": f"Дрон {drone_id} добавлен"}), 201
    return jsonify({"error": "Не передан id дрона"}), 404

@app.route("/drones/<drone_id>/takeoff", methods=["POST"])
def takeoff_drone(drone_id):
    """
    Отправляет команду взлета конкретному дрону.

    :param drone_id: идентификатор дрона
    :return: JSON-ответ с сообщением об успешном взлете и статус-код 200,
             или ошибка 404, если дрон не зарегистрирован,
             или ошибка 500, если произошла ошибка при взлете
    """
    if drone_id not in drones:
        return jsonify({"error": f"Дрон c id: {drone_id} не зарегистрирован"}), 404
    altitude = request.json.get("altitude")
    drone_info = drones[drone_id]
    drone_url = drone_info["control_url"] + "/takeoff"
    response = requests.post(drone_url, json={"altitude": altitude})
    if response.status_code == 200:
        return jsonify({"message": response.json().get("message")}), 200
    return jsonify({"error": f"Ошибка взлета дрона id: {drone_id}"}), 500

if __name__ == '__main__':
    # Запускаем Flask сервер с отладкой
    app.run(debug=True)
