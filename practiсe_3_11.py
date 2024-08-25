import airsim  # Импорт библиотеки AirSim для управления дроном и взаимодействия с симулятором
import os
import cv2
import numpy as np

# Создание клиента для взаимодействия с мультикоптером в AirSim
client = airsim.MultirotorClient()
client.confirmConnection()  # Подтверждение соединения с симулятором

# Запрос изображений с камеры дрона (0 - идентификатор камеры)
responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])

# Проверка, что получен ответ от симулятора
if responses:
    response = responses[0]  # Получение первого изображения из списка ответов

    # Преобразование изображения из формата 1D в 3D массив (RGB)
    img_1D = np.frombuffer(response.image_data_uint8, dtype=np.uint8)  # Конвертация байтового буфера в массив NumPy
    img_rgb = img_1D.reshape(response.height, response.width, 3)  # Изменение формы массива в соответствии с высотой, шириной и 3 каналами (RGB)

    # Сохранение изображения на диск
    cv2.imwrite('test.jpg', img_rgb)  # Сохранение изображения в файл 'test.jpg'
    print("Image saved")  # Сообщение об успешном сохранении изображения
else:
    print("No images found")  # Сообщение, если изображения не найдены