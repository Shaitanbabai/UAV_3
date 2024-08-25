import requests

# Определяем базовый URL для взаимодействия с сервером дронов
BASE_URL = 'http://localhost:5000/drones'

def takeoff(drone_id, altitude):
    """
    Функция для отправки команды взлета дрону.

    :param drone_id: идентификатор дрона, которому отправляется команда взлета
    :param altitude: высота, на которую должен подняться дрон
    :return: ответ сервера в формате JSON
    """
    # Формируем URL для отправки команды взлета
    url = f"{BASE_URL}/{drone_id}/takeoff"
    # Формируем полезную нагрузку с параметром высоты
    payload = {'altitude': altitude}
    # Отправляем POST-запрос с полезной нагрузкой в формате JSON
    response = requests.post(url, json=payload)
    # Возвращаем ответ сервера в формате JSON
    return response.json()

if __name__ == '__main__':
    # Определяем идентификатор дрона
    drone_id = "drone_index"
    # Задаем высоту для взлета дрона
    altitude = 200

    # Вызываем функцию взлета и получаем ответ сервера
    response = takeoff(drone_id, altitude)
    # Выводим сообщение от сервера
    print(f"Ответ сервера: {response.get('message')}")
