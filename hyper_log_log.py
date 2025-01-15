import json
import time
from datasketch import HyperLogLog


# Функція для точного підрахунку унікальних IP-адрес
def exact_unique_ips(log_file):
    ip_set = set()
    with open(log_file, 'r') as f:
        for line in f:
            try:
                log_entry = json.loads(line)
                ip_set.add(log_entry.get("remote_addr", None))
            except json.JSONDecodeError:
                continue  # Ігноруємо некоректні рядки
    return len(ip_set)


# Функція для наближеного підрахунку за допомогою HyperLogLog
def hyperloglog_unique_ips(log_file, p=11):  # p задає точність
    hll = HyperLogLog(p)  # Створення об'єкта HyperLogLog з точністю
    with open(log_file, 'r') as f:
        for line in f:
            try:
                log_entry = json.loads(line)
                ip = log_entry.get("remote_addr", None)
                if ip:
                    hll.update(ip.encode('utf-8'))  # Додавання елементів (IP)
            except json.JSONDecodeError:
                continue  # Ігноруємо некоректні рядки
    # Повертаємо оцінку кількості унікальних елементів
    return hll.count()  # Використовуємо count() для підрахунку


# Завантаження даних і підрахунок часу для кожного методу
log_file = "lms-stage-access.log"  # Шлях до вашого файлу

# Точний підрахунок
start_time = time.time()
exact_count = exact_unique_ips(log_file)
exact_time = time.time() - start_time

# HyperLogLog
start_time = time.time()
hll_count = hyperloglog_unique_ips(log_file)
hll_time = time.time() - start_time

# Виведення результатів
print("Результати порівняння:")
print(f"{'Точний підрахунок':>48} {'HyperLogLog':>14}")
print(f"{'Унікальні елементи':<30} {exact_count:<20} {hll_count:<20}")
print(f"{'Час виконання (сек.)':<30} {exact_time:<20.2f} {hll_time:<20.2f}")
