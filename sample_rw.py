from custom_csv import CustomCsvWriter, CustomCsvReader

# Write a sample CSV
with CustomCsvWriter("sample.csv") as w:
    w.writerow(["id", "name", "comment"])
    w.writerow(["1", "Alice", "hello, world"])
    w.writerow(["2", "Bob", 'He said "hi"'])

# Read it back
with CustomCsvReader("sample.csv") as r:
    for row in r:
        print(row)
