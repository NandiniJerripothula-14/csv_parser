Custom CSV Parser (Reader & Writer) – Python Implementation

This project implements a custom CSV reader and writer from scratch, without using Python's built-in csv module.
It demonstrates fundamental parsing techniques such as:

Handling quoted fields

Supporting escaped quotes ("")

Managing embedded newlines inside fields

Character-by-character streaming

Correct CSV serialization and escaping rules

A performance benchmark is also included to compare this custom implementation against Python’s highly optimized built-in csv module.

📘 Project Overview

This project includes the following components:

CustomCsvReader

A fully streaming CSV parser implemented as a Python iterator (__iter__ / __next__).
It correctly handles:

Commas inside fields

Fields enclosed in double quotes

Escaped double quotes ("")

Newlines within quoted fields

Character-by-character state-based parsing

The reader processes data incrementally, without loading the full file into memory.

CustomCsvWriter

A CSV writer that produces fully compliant CSV output. It:

Escapes embedded quotes

Automatically quotes fields containing:

Commas

Quotes

Newlines

Writes well-formed CSV output readable by standard tools

Benchmark Script

A performance benchmarking script that compares:

CustomCsvReader vs csv.reader

CustomCsvWriter vs csv.writer

The benchmark uses a large synthetic dataset and reports read/write execution times to evaluate performance differences.