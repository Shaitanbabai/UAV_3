import pandas as pd
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import seaborn as sns

telemetry_model_1 = pd.read_csv("model1_telemetry.csv")
telemetry_model_2 = pd.read_csv("model2_telemetry.csv")

# print(telemetry_model_1.describe().T)
# print(telemetry_model_2.describe().T)

telemetry_model_1["timestamp"] = pd.to_datetime(telemetry_model_1["timestamp"])
telemetry_model_2["timestamp"] = pd.to_datetime(telemetry_model_1["timestamp"])

# Анализ полета
flight_duration_model_1 = (telemetry_model_1['timestamp'].iloc[-1] -
                           telemetry_model_1['timestamp'].iloc[0]).total_seconds() / 60
flight_duration_model_2 = (telemetry_model_2['timestamp'].iloc[-1] -
                           telemetry_model_2['timestamp'].iloc[0]).total_seconds() / 60

print(f"Время полета Модель 1: {flight_duration_model_1}")
print(f"Время полета Модель 2: {flight_duration_model_2}")

battery_usage_model_1 = (telemetry_model_1['battery_life'].iloc[0] -
                        telemetry_model_1['battery_life'].iloc[-1])
battery_usage_model_2 = (telemetry_model_2['battery_life'].iloc[0] -
                        telemetry_model_2['battery_life'].iloc[-1])

print(f"Расход батареи Модель 1: {battery_usage_model_1}%")
print(f"Расход батареи Модель 2: {battery_usage_model_2}%")


def calc_dist(df):
    total_dist = 0
    for i in range(1, len(df)):
        start = (df.iloc[i-1]["latitude"], df.iloc[i-1]["longitude"])
        end = (df.iloc[i]["latitude"], df.iloc[i]["longitude"])
        total_dist += geodesic(start, end).meters
    return total_dist


dist_model_1 = calc_dist(telemetry_model_1)
dist_model_2 = calc_dist(telemetry_model_2)

print(f"Дистанция Модель 1: {dist_model_1}")
print(f"Дистанция Модель 2: {dist_model_2}")

eff_model_1 = dist_model_1 / battery_usage_model_1
eff_model_2 = dist_model_2 / battery_usage_model_2

print(f"Эффективность Модель 1: {eff_model_1}")
print(f"Эффективность Модель 2: {eff_model_2}")

plt.figure(figsize=(10, 5))
eff = [eff_model_1, eff_model_2]
models = ["Модель 1", "Модель 2"]
plt.bar(models, eff, color=["blue", "green"])
plt.xlabel("Модели дронов")
plt.ylabel("Эффективность дронов")
plt.title("Сравнение эффективности дронов")
plt.show()

plt.figure(figsize=(10, 5))
plt.plot(telemetry_model_1['longitude'], telemetry_model_1['latitude'], label="Модель 1", marker="o")
plt.plot(telemetry_model_2['longitude'], telemetry_model_2['latitude'], label="Модель 2", marker=".")
plt.xlabel("Широта")
plt.ylabel("Долгота")
plt.title("Путь дронов")
plt.show()

plt.figure(figsize=(14, 5))
# Высота
plt.subplot(1, 2, 1)
sns.lineplot(x="timestamp", y="altitude", data=telemetry_model_1, label="Модель 1")
sns.lineplot(x="timestamp", y="altitude", data=telemetry_model_2, label="Модель 2")
plt.xlabel("Время")
plt.ylabel("Высота")
plt.legend()

# Скорость
plt.subplot(1, 2, 2)
sns.lineplot(x="timestamp", y="speed", data=telemetry_model_1, label="Модель 1")
sns.lineplot(x="timestamp", y="speed", data=telemetry_model_2, label="Модель 2")
plt.xlabel("Время")
plt.ylabel("Скорость")
plt.legend()

plt.tight_layout()
plt.show()



