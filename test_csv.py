"""
Basic tests for the custom CSV reader and writer.

These tests:
- Check round-trip equality (write with CustomCsvWriter, read with CustomCsvReader).
- Compare against Python's csv module for correctness.
"""

import csv
import os
from typing import List

from custom_csv import CustomCsvReader, CustomCsvWriter


TEST_FILE = "test_data.csv"


def _roundtrip_and_compare(data: List[List[str]]) -> None:
    """Helper: write data, read back with both csv and custom, assert equality."""
    # Write using CustomCsvWriter
    with CustomCsvWriter(TEST_FILE) as writer:
        writer.writerows(data)

    # Read with standard csv.reader
    with open(TEST_FILE, "r", encoding="utf-8", newline="") as f:
        std_rows = list(csv.reader(f))

    # Read with CustomCsvReader
    with CustomCsvReader(TEST_FILE) as reader:
        custom_rows = list(reader)

    assert std_rows == data, "Standard csv.reader round-trip failed."
    assert custom_rows == data, "CustomCsvReader did not match written data."


def test_simple_rows() -> None:
    data = [
        ["Name", "Age"],
        ["Alice", "30"],
        ["Bob", "25"],
    ]
    _roundtrip_and_compare(data)


def test_commas_in_fields() -> None:
    data = [
        ["id", "description"],
        ["1", "value, with, commas"],
        ["2", "another,one"],
    ]
    _roundtrip_and_compare(data)


def test_quotes_in_fields() -> None:
    data = [
        ["id", "quote"],
        ["1", 'He said "hello"'],
        ["2", 'She replied "ok"'],
    ]
    _roundtrip_and_compare(data)


def test_newlines_in_fields() -> None:
    data = [
        ["id", "multiline"],
        ["1", "line1\nline2"],
        ["2", "single line"],
    ]
    _roundtrip_and_compare(data)


def run_all_tests() -> None:
    print("Running tests...")
    try:
        test_simple_rows()
        test_commas_in_fields()
        test_quotes_in_fields()
        test_newlines_in_fields()
        print("All tests passed!")
    finally:
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)


if __name__ == "__main__":
    run_all_tests()
