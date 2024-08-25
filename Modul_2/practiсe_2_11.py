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
        return sqlite3.connect(':memory:')

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

if __name__ == "__main__":
    # Создание объекта фабрики для SQLite и подключение к базе данных
    sql = SQLiteDBFactory()
    connection = sql.connect()
    cursor = connection.cursor()

    # Создание таблицы с автоматическим увеличением значения id
    cursor.execute("""
    CREATE TABLE tbl_drones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model TEXT,
        manufacturer TEXT,
        year INTEGER
    )
    """)

    # Данные для вставки в таблицу
    drone = {
        "model": "Model X",
        "manufacturer": "SkyCorp",
        "year": 2024,
    }

    # Создание INSERT-запроса с использованием QueryBuilder
    query_builder = QueryBuilder()
    insert_query = query_builder.insert_into("tbl_drones", ["model", "manufacturer", "year"]) \
                                .values(drone["model"], drone["manufacturer"], drone["year"]) \
                                .get_query()
    print(insert_query)  # Вывод сформированного запроса
    params = query_builder.get_params()  # Получение параметров для запроса
    cursor.execute(insert_query, params)  # Выполнение запроса с параметрами
    connection.commit()

    # Создание SELECT-запроса с использованием нового экземпляра QueryBuilder
    query_builder_select = QueryBuilder()
    select_query = query_builder_select.select("tbl_drones").get_query()
    cursor.execute(select_query)
    results = cursor.fetchall()

    # Вывод всех записей из таблицы
    for row in results:
        print(row)

    connection.close()  # Закрытие подключения к базе данных