import json
import time
from datasketch import HyperLogLog


def load_ips_from_log(file_path: str) -> list[str]:
    """Завантаження IP-адрес з лог-файлу"""
    ips = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            try:
                log_entry = json.loads(line.strip())
                ip = log_entry.get("remote_addr")
                if isinstance(ip, str):
                    ips.append(ip)
            except json.JSONDecodeError:
                continue  
    return ips


def exact_count(ips: list[str]) -> tuple[int, float]:
    start = time.time()
    result = len(set(ips))
    duration = time.time() - start
    return result, duration


def hyperloglog_count(ips: list[str], precision: int = 0.01) -> tuple[float, float]:
    hll = HyperLogLog(p=14)  
    start = time.time()
    for ip in ips:
        hll.update(ip.encode('utf-8'))
    result = hll.count()
    duration = time.time() - start
    return result, duration


def print_comparison_table(exact_num, exact_time, hll_num, hll_time):
    """Вивід таблиці з результатами"""
    print("\nРезультати порівняння:")
    print(f"{'':<30}{'Точний підрахунок':<20}{'HyperLogLog'}")
    print(f"{'Унікальні елементи':<30}{exact_num:<20}{hll_num:.0f}")
    print(f"{'Час виконання (сек.)':<30}{exact_time:<20.5f}{hll_time:.5f}")



if __name__ == "__main__":
    file_path = "hyper_log_log_compare/lms-stage-access.log"
    ips = load_ips_from_log(file_path)

    exact_result, exact_duration = exact_count(ips)
    hll_result, hll_duration = hyperloglog_count(ips)

    print_comparison_table(exact_result, exact_duration, hll_result, hll_duration)
