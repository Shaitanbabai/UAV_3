from flask import Flask, Response, request, jsonify

# Управление дронами

# GET
# /drones
# /drones/{drone_id}

# POST
# /drones

# PUT
# /drones/{drone_id}

# DELETE
# /drones/{drone_id}


# Управление полетом

# POST
# /drones/{drone_id}/takeoff
# /drones/{drone_id}/land
# /drones/{drone_id}/move

# GET
# /drones/{drone_id}/sensors

# Пример взлет
# POST /drones/{drone_id}/takeoff
# {
#     "altitude": 10
# }

app = Flask(__name__)

drones = {}


@app.route("/drones", methods=["GET"])
def get_drones():
    return jsonify(drones), 200


@app.route("/drones/<drone_id>", methods=["GET"])
def get_drone(drone_id):
    drone = drones.get(drone_id)
    if drone:
        return jsonify(drone), 200
    return jsonify({"error": "Дрон не найден"}), 404


@app.route("/drones", methods=["POST"])
def create_drone():
    drone_id = request.json.get("drone_id")
    if drone_id:
        drones[drone_id] = request.json
        return jsonify({"message": f"Дрон {drone_id} добавлен"}), 201
    return jsonify({"error": "Не передан id дрона"}), 404


if __name__ == '__main__':
    app.run(debug=True)
