from abc import ABC, abstractmethod
import sqlite3

# Паттерн Абстрактная фабрика для создания подключений к базе данных
class DBFactory(ABC):
    @abstractmethod
    def connect(self):
        pass

class SQLiteDBFactory(DBFactory):
    # Реализация метода connect для SQLite, создающая подключение к базе данных в памяти
    def connect(self):
        return sqlite3.connect('test.db')

# Паттерн Строитель для создания SQL-запросов
class QueryBuilder:
    def __init__(self):
        # Инициализация частями запроса
        self._query = {
            "select": None,
            "from": None,
            "where": None,
            "order_by": None,
            "insert_into": None,
            "values": None
        }
        self._params = []  # Список для хранения параметров запроса

    def select(self, table, columns="*"):
        # Метод для создания SELECT части запроса
        self._query["select"] = f"SELECT {columns}"
        self._query["from"] = f"FROM {table}"
        return self  # Возвращает объект QueryBuilder для цепочки вызовов

    def where(self, condition, parameters=None):
        # Метод для создания WHERE части запроса
        self._query["where"] = f"WHERE {condition}"
        if parameters:
            self._params.extend(parameters)  # Добавление параметров к запросу
        return self

    def order_by(self, order):
        # Метод для создания ORDER BY части запроса
        self._query["order_by"] = f"ORDER BY {order}"
        return self

    def add_params(self, *parameters):
        # Метод для добавления дополнительных параметров
        self._params.extend(parameters)
        return self

    def insert_into(self, table, columns):
        # Метод для создания INSERT INTO части запроса
        cols = ",".join(columns)
        placeholders = ",".join(["?"] * len(columns))
        self._query["insert_into"] = f"INSERT INTO {table} ({cols})"
        self._query["values"] = f"VALUES ({placeholders})"
        return self

    def values(self, *values):
        # Метод для добавления значений для вставки
        self._params.extend(values)
        return self

    def get_query(self):
        # Метод для сборки и получения итогового SQL-запроса
        query = ""
        if self._query["select"]:
            query = f"{self._query['select']} {self._query['from']}"
        if self._query["where"]:
            query += f" {self._query['where']}"
        if self._query["order_by"]:
            query += f" {self._query['order_by']}"
        if self._query["insert_into"]:
            query = f"{self._query['insert_into']} {self._query['values']}"
        return query

    def get_params(self):
        # Метод для получения списка параметров
        return self._params


# Паттерн ORM
class User:
    def __init__(self, id, name_operator, contact, comment):
        self.id = id
        self.name_operator = name_operator
        self.contact = contact
        self.comment = comment


class UserMapper:
    def __init__(self, connetion):
        self.connetion = connetion

    def get_user(self, id):
        cursor = self.connetion.cursor()
        cursor.execute(f"SELECT * FROM tbl_operators WHERE id={id}")
        result = cursor.fetchone()
        if result:
            return User(id=result[0], name_operator=result[1], contact=result[2], comment=result[3])
        return None

    def add_user(self, user: User):
        cursor = self.connetion.cursor()
        cursor.execute(f"INSERT INTO tbl_operators (name_operator, contact, comment) VALUES (?, ?, ?)",
                       (user.name_operator, user.contact, user.comment))

# Паттерн Хранитель для управления соединениями с БД
class DBConnectionManager:
    def __init__(self, factory):
        self.factory = factory
        self.connection = None

    def get_connection(self):
        # Метод для получения подключения к базе данных
        if self.connection is None:
            self.connection = self.factory.connect()
        return self.connection

    def close_connection(self):
        # Метод для закрытия подключения к базе данных
        if self.connection:
            self.connection.close()
            self.connection = None



if __name__ == "__main__":

    # Создание объекта фабрики для SQLite и подключение к базе данных
    factory = SQLiteDBFactory()
    connection_manager = DBConnectionManager(factory)
    connection = connection_manager.get_connection()
    cursor = connection.cursor()

    # Создание таблицы для тестирования
    cursor.execute('''CREATE TABLE IF NOT EXISTS tbl_drones (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      model TEXT NOT NULL,
                      manufacturer TEXT NOT NULL,
                      purchase_date INTEGER NOT NULL,
                      max_altitude INTEGER NOT NULL,
                      max_speed INTEGER NOT NULL,
                      max_flight_time INTEGER NOT NULL,
                      serial_number TEXT NOT NULL UNIQUE)''')
    connection.commit()

    # Данные для вставки в таблицу
    drone = {
        "model": "Model Y",
        "manufacturer": "DronInc",
        "purchase_date": 2023,
        "max_altitude": 250,
        "max_speed": 50,
        "max_flight_time": 30,
        "serial_number": "FDSF43FDSFSD",
    }

    try:
        # Создание INSERT-запроса с использованием QueryBuilder
        query_builder = QueryBuilder()
        insert_query = query_builder.insert_into("tbl_drones",
                                                 ["model", "manufacturer", "serial_number",
                                                  "purchase_date", "max_altitude", "max_speed", "max_flight_time"]) \
                                    .values(drone["model"],
                                            drone["manufacturer"],
                                            drone["serial_number"],
                                            drone["purchase_date"],
                                            drone["max_altitude"],
                                            drone["max_speed"],
                                            drone["max_flight_time"]) \
                                    .get_query()
        print(insert_query)  # Вывод сформированного запроса
        params = query_builder.get_params()  # Получение параметров для запроса
        cursor.execute(insert_query, params)  # Выполнение запроса с параметрами
        connection.commit()
    except Exception as e:
        print(f"Ошибка! Незвозможно добавить запись: {e}")

    # Создание SELECT-запроса с использованием нового экземпляра QueryBuilder
    query_builder_select = QueryBuilder()
    select_query = query_builder_select.select("tbl_drones").get_query()
    cursor.execute(select_query)
    results = cursor.fetchall()

    # Вывод всех записей из таблицы
    for row in results:
        print(row)

    connection_manager.close_connection()  # Закрытие подключения к базе данных