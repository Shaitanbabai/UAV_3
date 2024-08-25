import requests

# Определяем базовый URL для взаимодействия с сервером дронов
BASE_URL = 'http://localhost:3000'


def send_command(command):
    try:
        response = requests.get(f"{BASE_URL}/{command}")
        if response.status_code == 200:
            data = response.json()
            print("Сервер возвращает дату: ", data)
        else:
            print(response.status_code)
    except requests.exceptions.RequestException as e:
        print(e)

if __name__ == '__main__':
    send_command("time")
    send_command("1/takeoff")
