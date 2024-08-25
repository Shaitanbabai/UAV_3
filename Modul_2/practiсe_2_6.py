# Паттерн Наблюдатель
from abc import ABC, abstractmethod
import cv2

# Абстрактный класс для наблюдателей
class Observer(ABC):
    @abstractmethod
    def update(self, message: str, image=None):
        pass

# Класс, за которым наблюдают (Observable)
class Observable:
    def __init__(self):
        self._observers = []

    # Добавление наблюдателя
    def add_observer(self, observer: Observer):
        self._observers.append(observer)

    # Удаление наблюдателя
    def remove_observer(self, observer: Observer):
        self._observers.remove(observer)

    # Уведомление всех наблюдателей о событии
    def notify_observers(self, message: str, image=None):
        for observer in self._observers:
            observer.update(message, image)

# Наблюдатель для записи данных
class DataLogger(Observer):
    def update(self, message: str, image=None):
        print(f"Система записи получила сообщение: {message}")
        if image is not None:
            self.save_image(image)

    @staticmethod
    def save_image(image):
        filename = "camera.png"
        cv2.imwrite(filename, image)
        print(f"Снимок сохранен как {filename}!")

# Наблюдатель для системы предупреждений
class AlertSystem(Observer):
    def update(self, message: str, image=None):
        print(f"Система предупреждений получила сообщение: {message}")

# Наблюдатель для системы анализа
class AnalysisSystem(Observer):
    def update(self, message: str, image=None):
        print(f"Система анализа получила сообщение: {message}")

# Класс камеры, которая может уведомлять наблюдателей о событиях
class Camera(Observable):
    def __init__(self):
        super().__init__()
        self._zoom_lvl = 1.0

    # Метод для установки уровня зума
    def set_zoom(self, zoom_lvl: float):
        self._zoom_lvl = zoom_lvl
        self.notify_observers(f"Уровень зума изменен на {self._zoom_lvl}")

    # Метод для захвата изображения
    def take_image(self):
        caption = cv2.VideoCapture(0)
        ret, frame = caption.read()
        if ret:
            self.notify_observers("Захвачено изображение!", frame)
        caption.release()

# Создание объектов наблюдателей
data_logger = DataLogger()
alert_system = AlertSystem()
analysis_system = AnalysisSystem()

# Создание объекта камеры и добавление наблюдателей
camera = Camera()
camera.add_observer(data_logger)
camera.add_observer(alert_system)
camera.add_observer(analysis_system)

# Изменение зума камеры и захват изображения
camera.set_zoom(2.0)
camera.take_image()
