import hashlib


class BloomFilter:
    def __init__(self, size, num_hashes):
        """
        Ініціалізація фільтра Блума.
        :param size: Розмір бітового масиву.
        :param num_hashes: Кількість хеш-функцій.
        """
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def _hashes(self, item):
        """
        Генерація хешів для заданого елемента.
        :param item: Елемент для хешування.
        :return: Список індексів у бітовому масиві.
        """
        hashes = []
        for i in range(self.num_hashes):
            hash_value = int(hashlib.md5((str(i) + item).encode()).hexdigest(), 16)
            hashes.append(hash_value % self.size)
        return hashes

    def add(self, item):
        """
        Додавання елемента до фільтра Блума.
        :param item: Елемент для додавання.
        """
        for hash_index in self._hashes(item):
            self.bit_array[hash_index] = 1

    def contains(self, item):
        """
        Перевірка, чи є елемент у фільтрі Блума.
        :param item: Елемент для перевірки.
        :return: True, якщо елемент може бути у фільтрі; False, якщо точно немає.
        """
        return all(self.bit_array[hash_index] for hash_index in self._hashes(item))


def check_password_uniqueness(bloom_filter, passwords):
    """
    Перевірка списку паролів на унікальність.
    :param bloom_filter: Екземпляр фільтра Блума.
    :param passwords: Список паролів для перевірки.
    :return: Словник з результатами перевірки.
    """
    results = {}
    for password in passwords:
        if not password or not isinstance(password, str):
            results[password] = "некоректний пароль"
        elif bloom_filter.contains(password):
            results[password] = "вже використаний"
        else:
            results[password] = "унікальний"
            bloom_filter.add(password)
    return results


if __name__ == "__main__":
    # Ініціалізація фільтра Блума
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Додавання існуючих паролів
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    # Перевірка нових паролів
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Виведення результатів
    for password, status in results.items():
        print(f"Пароль '{password}' — {status}.")
