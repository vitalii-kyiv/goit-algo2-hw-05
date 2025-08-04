import hashlib


class BloomFilter:
    def __init__(self, size: int, num_hashes: int):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def _hashes(self, item: str):
        result = []
        for i in range(self.num_hashes):
            hash_digest = hashlib.md5(f"{item}{i}".encode()).hexdigest()
            hash_int = int(hash_digest, 16)
            index = hash_int % self.size
            result.append(index)
        return result

    def add(self, item: str):
        if not isinstance(item, str) or item == "":
            return  
        for index in self._hashes(item):
            self.bit_array[index] = 1

    def __contains__(self, item: str):
        if not isinstance(item, str) or item == "":
            return False
        return all(self.bit_array[index] == 1 for index in self._hashes(item))


def check_password_uniqueness(bloom_filter: BloomFilter, password_list: list[str]) -> dict:
    results = {}
    for pwd in password_list:
        if not isinstance(pwd, str) or pwd == "":
            results[pwd] = "некоректне значення"
        elif pwd in bloom_filter:
            results[pwd] = "вже використаний"
        else:
            results[pwd] = "унікальний"
            bloom_filter.add(pwd)
    return results


if __name__ == "__main__":
    bloom = BloomFilter(size=1000, num_hashes=3)

    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    for password, status in results.items():
        print(f"Пароль '{password}' — {status}.")
