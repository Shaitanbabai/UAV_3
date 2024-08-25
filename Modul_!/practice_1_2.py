import random

altitude = 0  # Высота в метрах
speed = 0  # Скорость в метрах в секунду
weight = 1.5  # Вес БПЛА в килограммах
payload = 500  # Грузоподъемность в граммах

pitch = 0  # Тангаж в градусах
roll = 0  # Крен в градусах
yaw = 0  # Рысканье в градусах

battery_capacity = 100  # Емкость батареи в процентах
# Против часовой стрелки (CCW)
# По часовой стрелке (CW)
# (1)       (2)
#  CCW      CW
#   \        /
#    \      /
#     ------
#    /      \
#   /        \
#  CW       CCW
# (3)       (4)

# int - целое
# float - вещественное
# str - строка
# list - список
propellers_speed = [0, 0, 0, 0] # Скорость вращения пропеллеров в об/мин
# print(propellers_speed[0]) - извлечь скорость 1 пропеллера

direction = 0  # Направление
is_flying = False  # Летит ли БПЛА
is_connected = False  # Подключен ли БПЛА
is_armed = False # Арминг двигателя

info = f"""
-------Квадрокоптер-------
Высота: {altitude} м, Скорость: {speed} м/сек.
Вес БПЛА: {weight} кг, Грузоподъемность: {speed} гр.
Тангаж: {pitch}, Крен: {roll} Рысканье: {yaw}
Скорость вращения пропеллеров: {propellers_speed}
({propellers_speed[0]})       ({propellers_speed[1]})
 CCW      CW
  \        /
   \      /
    ------
   /      \\
  /        \\
 CW       CCW
({propellers_speed[2]})       ({propellers_speed[3]})
"""

def drone_connect():
    global is_connected
    print("Подключение к БПЛА...")
    is_connected = True
    print("Подключение установлено")

def arm_drone():
    global is_armed, propellers_speed
    if is_connected == True:
        print("Армирование двигателя...")
        # Симулируем проверку безопасности
        print("Проверка безопасности")
        is_armed = True
        propellers_speed = [random.randint(0, 100),
                            random.randint(0, 100),
                            random.randint(0, 100),
                            random.randint(0, 100)]  # Скорость вращения пропеллеров в об/мин

print(info)
drone_connect()
arm_drone()
info = f"""
-------Квадрокоптер-------
Высота: {altitude} м, Скорость: {speed} м/сек.
Вес БПЛА: {weight} кг, Грузоподъемность: {speed} гр.
Тангаж: {pitch}, Крен: {roll} Рысканье: {yaw}
Скорость вращения пропеллеров: {propellers_speed}
({propellers_speed[0]})       ({propellers_speed[1]})
 CCW      CW
  \        /
   \      /
    ------
   /      \\
  /        \\
 CW       CCW
({propellers_speed[2]})       ({propellers_speed[3]})
"""
print(info)