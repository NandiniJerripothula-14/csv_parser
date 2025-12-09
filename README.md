# 🚀 Custom CSV Reader & Writer (Python)

## 📌 Overview

This project implements a **custom CSV reader and writer from scratch** in Python.  
It demonstrates how CSV parsing works internally — especially how to correctly handle:

- Comma-separated fields  
- Fields enclosed in double quotes  
- Escaped quotes (`""` → `"`)  
- Newlines inside quoted fields  
- Streaming reads (line-by-line processing)

The project also includes a **benchmark** comparing the custom implementation with Python’s built-in `csv` module.

---

## 📁 Project Structure

```text
csv_parser/
│
├── custom_csv.py        # Core CSV reader & writer implementation
├── benchmark.py         # Performance comparison with Python's csv module
├── test_csv.py          # Functional tests for correctness
├── sample_rw.py         # Small demo showing reading & writing
├── requirements.txt     # Dependencies (Python only)
└── README.md            # Documentation (this file)


---
```

## 🚀 Features

### **CustomCsvReader**
- Iterator-based reader (`__iter__`, `__next__`)
- Handles:
  - Commas inside fields  
  - Quoted fields  
  - Escaped quotes (`""`)  
  - Newlines inside fields  
- Uses a **state machine** for accurate parsing  
- Reads file **character by character**  
- Streams data efficiently (no full file load)

### **CustomCsvWriter**
- Writes rows to CSV format
- Automatically quotes fields containing:
  - Commas  
  - Quotes  
  - Newlines  
- Escapes internal quotes by doubling them  
- Output compatible with Python's built-in `csv` module

### **Benchmark**
- Generates synthetic CSV file (10,000 rows × 5 columns)
- Compares:
  - Read speed: Custom vs Python csv
  - Write speed: Custom vs Python csv
- Prints clean average runtime results

### **Tests**
Covers:
- Basic rows  
- Commas in fields  
- Quotes in fields  
- Multiline fields  
- Round-trip validation (`write → read → match`)

---

## 📦 Installation

No external dependencies are required.  
Make sure you have **Python 3.8+** installed.

```bash
git clone <your-repository-url>
cd csv_parser
pip install -r requirements.txt
```
🧪 Running Tests

To verify correctness:
```
python test_csv.py
```

Expected output:

Running tests...
All tests passed!

⚡ Running the Benchmark
```
python benchmark.py
```
Example output (will vary):
```
=== READ BENCHMARK (average over runs) ===
CustomCsvReader avg: 0.1805 seconds
csv.reader      avg: 0.0452 seconds

=== WRITE BENCHMARK (average over runs) ===
CustomCsvWriter avg: 0.0953 seconds
csv.writer      avg: 0.0328 seconds
```
🔍 Benchmark Interpretation

Python’s csv module is significantly faster — this is expected because it is written in optimized C.

The custom implementation is still quite efficient and is excellent for:

Educational purposes

Custom CSV formats

Understanding parsing internals

📘 Usage Examples
✏️ Writing CSV
```
from custom_csv import CustomCsvWriter

rows = [
    ["id", "name", "comment"],
    ["1", "Alice", "hello, world"],
    ["2", "Bob", "He said \"hi\""],
    ["3", "Carol", "line1\nline2"],
]

with CustomCsvWriter("output.csv") as writer:
    writer.writerows(rows)
```
📖 Reading CSV
```
from custom_csv import CustomCsvReader

with CustomCsvReader("output.csv") as reader:
    for row in reader:
        print(row)
```
Example output:
```
['id', 'name', 'comment']
['1', 'Alice', 'hello, world']
['2', 'Bob', 'He said "hi"']
['3', 'Carol', 'line1', 'line2']
```
🏗 Internal Design Notes
🔹 Parsing Strategy (Reader)

The reader uses a character-by-character state machine:

in_quotes = True → delimiter and newline are treated as literal characters

"" sequence → converted into a single "

Proper handling of:

CR (\r)

LF (\n)

CRLF (\r\n)

🔹 Writing Strategy (Writer)

Check if a field needs quoting

Replace " with "" inside fields

Wrap field in double quotes if necessary

Join fields using the chosen delimiter

🎓 Educational Value

This project teaches:

Low-level CSV parsing logic

String processing

State machine design

File I/O handling

Benchmarking in Python

Writing robust parsing logic for real-world applications

🙌 Acknowledgements

Inspired by:

The CSV standard (RFC 4180)

Python’s built-in csv module

📜 License

Free to use for learning, submissions, and educational purposes.
