import psutil
import time
import pandas as pd
from datetime import datetime


def get_cpu_temp():
    """Получение температуры CPU"""
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = float(f.read().strip()) / 1000.0
        return temp
    except:
        return None


def classify_workload(cpu_percent):
    """Классификация типа нагрузки"""
    if cpu_percent < 20:
        return 'idle'
    elif 20 <= cpu_percent < 70:
        return 'work'
    else:
        return 'gaming'


def collect_data(interval=5):
    """Сбор данных с заданным интервалом"""
    data = []

    try:
        while True:
            # Получение данных
            timestamp = datetime.now()
            cpu_temp = get_cpu_temp()
            cpu_percent = psutil.cpu_percent()
            workload_type = classify_workload(cpu_percent)

            if cpu_temp is not None:
                data.append([
                    timestamp,
                    cpu_temp,
                    cpu_percent,
                    workload_type
                ])
                print(f"Собрано: {timestamp} | {cpu_temp}°C | {cpu_percent}% | {workload_type}")

            time.sleep(interval)
    except KeyboardInterrupt:
        # Сохранение в CSV при завершении
        df = pd.DataFrame(data, columns=['timestamp', 'temperature', 'cpu_percent', 'workload_type'])
        df.to_csv('cpu_data.csv', index=False)
        print("Данные сохранены в cpu_data.csv")


if __name__ == "__main__":
    collect_data(interval=10)  # Интервал в секундах