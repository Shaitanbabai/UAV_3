from practiсe_3_13 import *
import jwt

class SafetyCheck(ICommand):
    def __init__(self, secret_key: str):
        self.__secret_key = secret_key

    def __call__(self, command: ICommand, token: str):
        self.__command = command
        self.__token = token
        return self

    def execute(self):
        if self.check_token():
            print("Команда принята")
            self.__command.execute()
        else:
            print("Команда отклонена: провал проверки безопасности")

    def check_token(self):
        print("Проверка безопасности...")
        try:
            decode_token = jwt.decode(self.__token, self.__secret_key, algorithms=['HS256'])
            print(f"Токен действителен: {decode_token}")
            return True
        except jwt.InvalidTokenError as e:
            print("Токен недействителен!!!")
            return False


if __name__ == '__main__':
    drone_controller = DroneController()
    drone_context = DroneContext()

    secret_key = 'my_secret_key'
    token = jwt.encode({"sub": "drone_123"}, secret_key, algorithm='HS256')

    # SafetyCheck(Takeoff(drone_controller), token).execute()
    safety_check = SafetyCheck(secret_key)
    safety_check(Takeoff(drone_controller), token).execute()