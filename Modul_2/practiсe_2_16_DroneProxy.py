import jwt
import practiсe_2_15_Server
import time

# SECRET_KEY = 'myKEY-111'
SECRET_KEY_PART_1 = "myKEY"
SECRET_KEY_PART_2 = "-111"

def get_secret_key():
    return SECRET_KEY_PART_1 + SECRET_KEY_PART_2

class Drone:
    def fly(self):
        print("Дрон в полете")

    def takeoff(self):
        print("Взлет")

    def land(self):
        print("Приземление")

class DroneProxy:
    def __init__(self, drone, token):
        self._drone = drone
        self._token = token

    def verify_token(self):
        try:
            payload = jwt.decode(self._token, get_secret_key(), algorithms=['HS256'])
            return payload["user_id"]
        except jwt.ExpiredSignatureError:
            print("Токен истек")
            return None
        except jwt.InvalidTokenError:
            print("Токен не валиден")
            return None

    def takeoff(self):
        if self.verify_token():
            self._drone.takeoff()
        else:
            print("Доступ запрещен: ошибка авторизации")

    def land(self):
        if self.verify_token():
            self._drone.land()
        else:
            print("Доступ запрещен: ошибка авторизации")


def request_token(user_id):
    return practiсe_2_15_Server.generate_token(user_id)

user_id = "Egor1"
token = request_token(user_id)
print(f"{user_id} получили токен:\n{token}")

drone_1 = Drone()
proxy = DroneProxy(drone_1, token)
proxy.takeoff()

time.sleep(7)

proxy.land()