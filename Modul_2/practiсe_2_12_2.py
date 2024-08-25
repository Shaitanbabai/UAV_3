import sqlite3

connection = sqlite3.connect('test.db')
cursor = connection.cursor()

# Таблица "Дроны"
cursor.execute("""
CREATE TABLE IF NOT EXISTS tbl_drones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    max_altitude INTEGER,
    max_speed INTEGER,
    max_flight_time INTEGER,
    serial_number TEXT UNIQUE NOT NULL,
    payload INTEGER,
    model TEXT NOT NULL,
    manufacturer TEXT NOT NULL,
    purchase_date DATE,
    sofware_version TEXT,
    battery_capacity INTEGER,
    flight_hours INTEGER
)
""")

# Таблица "Статус"
cursor.execute("""
CREATE TABLE IF NOT EXISTS tbl_status (    
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
)
""")

# Таблица "Статус Дронов"
cursor.execute("""
CREATE TABLE IF NOT EXISTS tbl_drones_status (    
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    drone_id INTEGER NOT NULL,
    status_id INTEGER NOT NULL,
    mission_id INTEGER NOT NULL,
    operator_id INTEGER NOT NULL,
    status_update_time DATETIME NOT NULL,
    battery_level INTEGER NOT NULL,
    latitude REAL,
    longitude REAL,
    altitude REAL,
    direction REAL,
    is_flying BOOLEAN,
    FOREIGN KEY (drone_id) REFERENCES tbl_drones(id),
    FOREIGN KEY (status_id) REFERENCES tbl_status(id),
    FOREIGN KEY (mission_id) REFERENCES tbl_missions(id),
    FOREIGN KEY (operator_id) REFERENCES tbl_operators(id)
)
""")

# Таблица "Техническое обслуживание"
cursor.execute("""
CREATE TABLE IF NOT EXISTS tbl_maintenance (    
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    drone_id INTEGER NOT NULL,
    last_maintenance DATE,
    desription TEXT,    
    FOREIGN KEY (drone_id) REFERENCES tbl_drones(id)
)
""")

# Таблица "Миссии"
cursor.execute("""
CREATE TABLE IF NOT EXISTS tbl_missions (    
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_mission TEXT NOT NULL,
    name_mission TEXT UNIQUE NOT NULL,
    description TEXT,
    status TEXT NOT NULL,
    start_date DATETIME,
    end_date DATETIME
)
""")

# Таблица "Оператор"
cursor.execute("""
CREATE TABLE IF NOT EXISTS tbl_operators (    
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_operator TEXT UNIQUE NOT NULL,
    contact TEXT,
    comment TEXT
)
""")

connection.commit()
connection.close()


























