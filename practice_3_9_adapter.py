import requests
from abc import ABC, abstractmethod

class DroneAdapter(ABC):
    # Абстрактный класс, определяющий интерфейс для работы с дронами
    @abstractmethod
    def __init__(self, base_url):
        pass

    @abstractmethod
    def get_time(self):
        pass  # Метод для получения текущего времени с сервера

    @abstractmethod
    def takeoff(self):
        pass  # Метод для взлета дрона

    @abstractmethod
    def turn(self, degree):
        pass  # Метод для поворота дрона

class DroneAdapterNodejs(DroneAdapter):
    def __init__(self, base_url):
        self.base_url = base_url  # Сохраняем базовый URL для взаимодействия с сервером

    def get_time(self):
        try:
            response = requests.get(f"{self.base_url}/time")  # Выполняем GET-запрос для получения времени
            response.raise_for_status()  # Проверяем успешность запроса
            data = response.json()  # Парсим ответ сервера как JSON
            return data["time"]  # Возвращаем время из полученного ответа
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении времени: {e}")  # Обрабатываем возможные ошибки

    def takeoff(self, drone_id):
        try:
            response = requests.get(f"{self.base_url}/{drone_id}/takeoff")  # Выполняем GET-запрос для взлета дрона
            response.raise_for_status()  # Проверяем успешность запроса
            data = response.json()  # Парсим ответ сервера как JSON
            return data  # Возвращаем результат взлета
        except requests.exceptions.RequestException as e:
            print(f"Ошибка взлета: {e}")  # Обрабатываем возможные ошибки

    def turn(self, degree):
        pass  # Метод пока не реализован

if __name__ == '__main__':
    BASE_URL = 'http://localhost:3000'  # Базовый URL для сервера дронов

    nodejs = DroneAdapterNodejs(BASE_URL)  # Создаем экземпляр адаптера для Node.js
    print(nodejs.get_time())  # Выводим текущее время с сервера
    print(nodejs.takeoff(drone_id="1"))  # Отправляем команду на взлет дрону с ID "1"
