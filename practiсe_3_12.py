from abc import ABC, abstractmethod

# Абстрактный класс, который определяет интерфейс для различных API управления дроном
class IDroneAPI(ABC):
    def __init__(self, connect_uri=None):
        self.client = None  # Переменная для хранения клиента API
        self.connect_uri = connect_uri  # URI для подключения к дрону, если требуется

    @abstractmethod
    def connect(self):
        """Метод для подключения к дрону. Должен быть реализован в подклассах."""
        pass

    @abstractmethod
    def get_image(self, max_attempts=10, delay=1):
        """Метод для получения изображения с камеры дрона. Должен быть реализован в подклассах."""
        pass

import airsim
import numpy as np
import cv2

# Класс, реализующий API для работы с AirSim
class AirSimAPI(IDroneAPI):
    def connect(self):
        """Подключение к симулятору AirSim"""
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()  # Подтверждение соединения
        print("Подключение через Air Sim")

    def get_image(self, max_attempts=10, delay=1):
        """Получение изображения с камеры дрона в AirSim"""
        # Запрос изображения с камеры 0
        responses = self.client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])

        if responses:
            response = responses[0]

            # Преобразование изображения из байтового буфера в RGB-изображение
            img_1D = np.frombuffer(response.image_data_uint8, dtype=np.uint8)
            img_rgb = img_1D.reshape(response.height, response.width, 3)

            # Сохранение изображения на диск
            cv2.imwrite('test.jpg', img_rgb)
            print("Image saved")
        else:
            print("No images found")

from pymavlink import mavutil
import time

# Класс, реализующий API для работы с MAVLink
class MavLinkAPI(IDroneAPI):
    def connect(self):
        """Подключение к дрону через MAVLink"""
        self.client = mavutil.mavlink_connection(self.connect_uri)
        self.client.wait_heartbeat()  # Ожидание сигнала "heartbeat" от дрона
        print("Соединение с дроном установлено")

    def get_image(self, max_attempts=10, delay=1):
        """Получение изображения с камеры дрона через MAVLink"""
        # Отправка команды на захват изображения
        self.client.mav.command_long_send(
            self.client.target_system,
            self.client.target_component,
            mavutil.mavlink.MAV_CMD_IMAGE_START_CAPTURE,  # Команда для начала захвата изображения
            0,
            0,
            0,
            1,  # Количество кадров (1)
            0,
            0, 0, 0
        )

        # Ожидание получения изображения в течение нескольких попыток
        for _ in range(max_attempts):
            response = self.client.recv_match(type='CAMERA_IMAGE_CAPTURED', blocking=True, timeout=5)
            if response:
                print(f"Путь до фото: {response.file_path}")
                break
            else:
                print("Ожидание камеры...")
            time.sleep(delay)

# Фабрика для создания объектов различных API в зависимости от типа
class DroneAPIFactory:
    @staticmethod
    def get_drone_api(type_api, connect_uri):
        """Возвращает объект API в зависимости от типа"""
        if type_api == "AirSim":
            return AirSimAPI()
        elif type_api == "MavLink":
            return MavLinkAPI(connect_uri)
        else:
            raise ValueError("Такое API не реализовано")

if __name__ == '__main__':
    type_api = "MavLink"  # Выбор типа API ("AirSim" или "MavLink")
    connect_uri = "tcp://127.0.0.1:5555"  # URI для подключения к MAVLink
    drone = DroneAPIFactory.get_drone_api(type_api, connect_uri)  # Создание объекта API через фабрику
    drone.connect()  # Подключение к дрону
    drone.get_image()  # Получение изображения
