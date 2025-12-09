"""
Benchmark script for CustomCsvReader/CustomCsvWriter vs Python's csv module.

- Generates a synthetic CSV with 10,000 rows and 5 columns.
- Benchmarks:
    - Reading with CustomCsvReader vs csv.reader
    - Writing with CustomCsvWriter vs csv.writer
- Uses timeit with callables.
"""

import csv
import os
import random
import string
import timeit
from typing import List

from custom_csv import CustomCsvReader, CustomCsvWriter


DATA_FILE = "benchmark_data.csv"
CUSTOM_OUT_FILE = "custom_out.csv"
STD_OUT_FILE = "std_out.csv"


def _random_text(max_len: int = 20) -> str:
    """
    Generate a random string that sometimes includes commas, quotes, or newlines.
    This stresses the CSV parser.
    """
    base_chars = string.ascii_letters + string.digits
    special_chars = [",", '"', "\n"]
    length = random.randint(1, max_len)
    chars: List[str] = []
    for _ in range(length):
        if random.random() < 0.15:
            chars.append(random.choice(special_chars))
        else:
            chars.append(random.choice(base_chars))
    return "".join(chars)


def generate_synthetic_csv(
    path: str = DATA_FILE,
    num_rows: int = 10_000,
    num_cols: int = 5,
    seed: int = 42,
) -> None:
    """
    Generate a synthetic CSV file containing edge cases.

    Fields may contain:
    - commas
    - double quotes
    - embedded newlines
    """
    random.seed(seed)
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for _ in range(num_rows):
            row = [_random_text() for _ in range(num_cols)]
            writer.writerow(row)


def read_with_custom(path: str = DATA_FILE) -> int:
    """Read entire file with CustomCsvReader and return row count."""
    count = 0
    with CustomCsvReader(path) as reader:
        for _ in reader:
            count += 1
    return count


def read_with_std(path: str = DATA_FILE) -> int:
    """Read entire file with csv.reader and return row count."""
    count = 0
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        for _ in reader:
            count += 1
    return count


def load_data(path: str = DATA_FILE) -> List[List[str]]:
    """Load CSV using standard reader into memory for write benchmarks."""
    with open(path, "r", encoding="utf-8", newline="") as f:
        return list(csv.reader(f))


def write_with_custom(rows: List[List[str]], path: str = CUSTOM_OUT_FILE) -> None:
    """Write all rows to CSV using CustomCsvWriter."""
    with CustomCsvWriter(path) as writer:
        writer.writerows(rows)


def write_with_std(rows: List[List[str]], path: str = STD_OUT_FILE) -> None:
    """Write all rows to CSV using csv.writer."""
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def benchmark(num_runs: int = 5) -> None:
    """
    Run benchmarks and print a report.

    Args:
        num_runs: How many times to repeat each measurement.
    """
    if not os.path.exists(DATA_FILE):
        print(f"Generating synthetic CSV at {DATA_FILE}...")
        generate_synthetic_csv()

    print("Loading data into memory for write benchmarks...")
    rows = load_data()

    # ----------------- Read benchmark -----------------
    print("\n=== READ BENCHMARK (average over runs) ===")

    custom_read_time = timeit.timeit(
        stmt=lambda: read_with_custom(DATA_FILE),
        number=num_runs,
    ) / num_runs

    std_read_time = timeit.timeit(
        stmt=lambda: read_with_std(DATA_FILE),
        number=num_runs,
    ) / num_runs

    print(f"CustomCsvReader avg: {custom_read_time:.6f} seconds")
    print(f"csv.reader      avg: {std_read_time:.6f} seconds")

    # ----------------- Write benchmark -----------------
    print("\n=== WRITE BENCHMARK (average over runs) ===")

    custom_write_time = timeit.timeit(
        stmt=lambda: write_with_custom(rows, CUSTOM_OUT_FILE),
        number=num_runs,
    ) / num_runs

    std_write_time = timeit.timeit(
        stmt=lambda: write_with_std(rows, STD_OUT_FILE),
        number=num_runs,
    ) / num_runs

    print(f"CustomCsvWriter avg: {custom_write_time:.6f} seconds")
    print(f"csv.writer      avg: {std_write_time:.6f} seconds")


if __name__ == "__main__":
    benchmark()
