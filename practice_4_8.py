# 55.753789, 37.622576

from practice_4_7_1 import *

# pip install ultralytics
# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
import torch
import numpy as np
import pandas as pd
import cv2
import requests


class ObjectDetection:
    def __init__(self):
        self.__model = self.__load_model()
        self.classes = self.__model.names

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.__model.to(device)

    def __load_model(self):
        # У кого скачалась последняя версия torch и выдает ошибку:
        # from ultralytics import YOLO
        # model = YOLO('yolov5x.pt')
        model = torch.hub.load('ultralytics/yolov5', 'yolov5x', pretrained=True)
        return model

    def detect_objects(self, image_path):
        img = cv2.imread(image_path)
        if img is None:
            return

        results = self.__model(img)

        detections = results.xyxy[0].cpu().numpy()

        detected_objects = []
        for detection in detections:
            x1, y1, x2, y2, conf, class_id = detection
            label = f"{self.classes[class_id]} {conf:.2f}"
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(img, label, (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            detected_objects.append({
                "class": self.classes[class_id],
                "confidence": int(conf),
                "coordinates": (int(x1), int(y1), int(x2), int(y2))
            })

        cv2.imshow("Распознавание", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return img, detected_objects


if __name__ == '__main__':
    obj = ObjectDetection()

    img, detected_objects = obj.detect_objects('msk_4.jpg')
    # msk_1.jpg 37.613785 55.732919 азимут 40,  высота 60
    # msk_3.jpg 37.662941 55.732247 азимут 170, высота 30
    # msk_4.jpg 37.662941 55.732247 азимут 80,  высота 30
    # msk.webp 55.753789, 37.622576 азимут 180

    if detected_objects:
        print("Обнаружены объекты:")
        for obj in detected_objects:
            print(f'Класс: {obj["class"]}, вероятность: {obj["confidence"]*100:.0f}, координаты: {obj["coordinates"]}')
            h_object = 1.7
            altitude_drone = 30
            theta_vertical = -30
            theta_horizontal = 0
            fov_vertical = 45
            fov_horizontal = 60
            w_image = img.shape[1]
            h_image = img.shape[0]
            x1, y1, x2, y2 = obj["coordinates"]

            latitude_drone = 37.662941
            longitude_drone = 55.732247

            direction_drone = 80

            latitude_object, longitude_object = calc_coord(h_object,
                                                           altitude_drone,
                                                           theta_vertical,
                                                           theta_horizontal,
                                                           fov_vertical,
                                                           fov_horizontal,
                                                           w_image,
                                                           h_image,
                                                           x1, y1, x2, y2,
                                                           latitude_drone,
                                                           longitude_drone,
                                                           direction_drone)
            print(f"Обнаружен человек в координате: {latitude_object:.4f}, {longitude_object:.4f}")
