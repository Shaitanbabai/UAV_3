import numpy as np

# ID БПЛА | Время полета (минуты) | Расстояние (километры) |
# Средняя скорость (км/ч) | Высота полета (метры)
drones_data = np.array([
    [1, 30, 10, 20, 500],
    [2, 45, 15, 20, 600],
    [3, 25, 8, 19.2, 550],
    [4, 60, 25, 25, 700],
    [5, 35, 12, 20.6, 580]
])
print("Данные о полетах БПЛА:")
print(drones_data)

flight_time = drones_data[:, 1]
average_flight_time = np.mean(flight_time)
print(f"Среднее время полета: {average_flight_time} минут")


import pandas as pd

drones_data2 = {
    "ID БПЛА": [1, 2, 3, 4, 5],
    "Время полета": [30, 45, 25, 60, 35],
    "Расстояние": [10, 15, 8, 25, 12],
    "Средняя скорость": [20, 20, 19.2, 25, 20.6],
    "Высота полета": [500, 600, 550, 700, 580]
}

drones_df = pd.DataFrame(drones_data2)
print("\n-----------\n")
print("Данные о полетах БПЛА:")
print(drones_df)

average_flight_time = drones_df["Время полета"].mean()
print(f"Среднее время полета: {average_flight_time} минут")


import matplotlib.pyplot as plt

drones_df.plot(x='ID БПЛА', y="Время полета", kind='bar')
plt.xlabel('ID БПЛА')
plt.ylabel('Время полета (минуты)')
plt.title('Время полета БПЛА')
plt.show()