# Паттерн Адаптер
import xml.etree.ElementTree as ET
import json

# Класс для работы с данными сенсора в формате XML
class SensorXML:
    def __init__(self, path: str):
        self.path = path

    def get_data(self):
        # Чтение данных из XML-файла
        with open(self.path, "r", encoding="utf-8") as file:
            data = file.read()
        return data

# Адаптер для преобразования данных из формата XML в JSON
class JSONAdapter:
    def __init__(self, sensor_xml: SensorXML):
        self.sensor_xml = sensor_xml

    def get_data(self):
        # Получение данных из XML и их преобразование в JSON
        xml_data = self.sensor_xml.get_data()
        root = ET.fromstring(xml_data)
        return self.xml_to_json(root)

    # Метод для преобразования XML-данных в формат JSON
    @staticmethod
    def xml_to_json(root):
        dict_data = {}
        for element in root:
            dict_data[element.tag] = int(element.text)
        # Пример выходных данных: {"altitude": 1000, "speed": 150}
        return dict_data

# Использование адаптера для преобразования данных
sensor_data = SensorXML("sensor.xml")  # Исходные данные в формате XML
adapter = JSONAdapter(sensor_data)     # Преобразование данных через адаптер
json_data = adapter.get_data()         # Получение данных в формате JSON
print(json.dumps(json_data, indent=4)) # Вывод JSON-данных с форматированием
