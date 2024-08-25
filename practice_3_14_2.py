# https://habr.com/ru/articles/781866/

from practiсe_3_13 import *
import jwt

class SafetyCheck:
    def __init__(self, secret_key: str):
        self.__secret_key = secret_key

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            token = kwargs.get('token')
            if self.check_token(token):
                return func(*args, **kwargs)
            else:
                print("Команда отклонена: провал проверки безопасности")
                return None

        return wrapper

    def check_token(self, token):
        print("Проверка безопасности...")
        try:
            decode_token = jwt.decode(token, self.__secret_key, algorithms=['HS256'])
            print(f"Токен действителен: {decode_token}")
            return True
        except jwt.InvalidTokenError as e:
            print("Токен недействителен!!!")
            return False

@SafetyCheck(secret_key='my_secret_key')
def execute_drone_commands(*commands, token):
    for command in commands:
        command.execute()


if __name__ == '__main__':
    import time
    time.sleep(5)
    drone_controller = DroneController()
    drone_context = DroneContext()

    secret_key = 'my_secret_key'
    token = jwt.encode({"sub": "drone_123"}, secret_key, algorithm='HS256')

    # SafetyCheck(Takeoff(drone_controller), token).execute()
    # safety_check = SafetyCheck(secret_key)
    # safety_check(Takeoff(drone_controller), token).execute()
    execute_drone_commands(Takeoff(drone_controller),
                           MoveForward(drone_controller, 100),
                           Turn(drone_controller, 90),
                           token=token)