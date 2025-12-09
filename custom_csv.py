"""
Custom CSV reader and writer implementation.

This module provides:
- CustomCsvReader: iterator-based CSV reader with proper CSV parsing.
- CustomCsvWriter: CSV writer that handles quoting and escaping.

Features:
- Comma-delimited parsing.
- Double-quoted fields.
- Escaped quotes inside quoted fields ("").
- Newlines inside quoted fields.
- Streaming read: one row at a time.
"""

from __future__ import annotations

from typing import List, Optional, Sequence, Union


class CustomCsvReader:
    """
    Streaming CSV reader implemented as an iterator.

    This reader:
    - Parses comma-delimited CSV files.
    - Supports double-quoted fields.
    - Supports escaped quotes inside quoted fields ("" -> ").
    - Supports newlines inside quoted fields.
    - Reads in a streaming fashion: yields one row at a time.
    """

    def __init__(
        self,
        file_path: str,
        delimiter: str = ",",
        quotechar: str = '"',
        encoding: str = "utf-8",
    ) -> None:
        """
        Initialize the CSV reader.

        Args:
            file_path: Path to the CSV file.
            delimiter: Field delimiter character, default is comma.
            quotechar: Character used to quote fields, default is ".
            encoding: File encoding, default is "utf-8".
        """
        if len(delimiter) != 1:
            raise ValueError("Delimiter must be a single character.")
        if len(quotechar) != 1:
            raise ValueError("Quote character must be a single character.")

        self.file_path = file_path
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.encoding = encoding

        # Open file in text mode with newline='' to avoid automatic newline translation.
        self._fh = open(self.file_path, "r", encoding=self.encoding, newline="")
        self._peek_char: Optional[str] = None
        self._eof = False

    def __iter__(self) -> "CustomCsvReader":
        return self

    def __next__(self) -> List[str]:
        """
        Return the next CSV row.

        Raises:
            StopIteration: When the end of file is reached.
        """
        row = self._parse_next_row()
        if row is None:
            raise StopIteration
        return row

    # Python 2-style alias; harmless in Python 3.
    next = __next__

    def __enter__(self) -> "CustomCsvReader":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def close(self) -> None:
        """Close the underlying file."""
        if not self._fh.closed:
            self._fh.close()

    # ----------------------- Internal helpers -----------------------

    def _read_char(self) -> str:
        """
        Read and return the next character from the file, or '' on EOF.

        Respects the one-character peek buffer if it is set.
        """
        if self._peek_char is not None:
            ch = self._peek_char
            self._peek_char = None
            return ch

        ch = self._fh.read(1)
        if ch == "":
            self._eof = True
        return ch

    def _peek(self) -> str:
        """
        Return the next character without consuming it, or '' on EOF.
        """
        if self._peek_char is None:
            self._peek_char = self._fh.read(1)
            if self._peek_char == "":
                self._eof = True
        return self._peek_char or ""

    def _parse_next_row(self) -> Optional[List[str]]:
        """
        Parse and return the next CSV row as a list of strings.

        Returns:
            A list of field strings, or None if end of file is reached.
        """
        if self._eof:
            return None

        row: List[str] = []
        field_chars: List[str] = []
        in_quotes = False

        while True:
            ch = self._read_char()

            # EOF handling
            if ch == "":
                if in_quotes:
                    # Unterminated quoted field at EOF: treat as closed.
                    in_quotes = False
                if field_chars or row:
                    # Flush last field if any content or if we already have fields.
                    row.append("".join(field_chars))
                    return row
                # Truly no more data
                return None

            if in_quotes:
                # We are inside a quoted field
                if ch == self.quotechar:
                    # Could be end of quoted field or escaped quote
                    next_ch = self._peek()
                    if next_ch == self.quotechar:
                        # Escaped quote: consume the peeked char and append a single quote
                        self._read_char()
                        field_chars.append(self.quotechar)
                    else:
                        # End of quoted field
                        in_quotes = False
                else:
                    field_chars.append(ch)
                continue

            # Not in quotes
            if ch == self.delimiter:
                # End of field
                row.append("".join(field_chars))
                field_chars = []
            elif ch == self.quotechar:
                # Start of a quoted field if field is empty so far,
                # otherwise treat as literal character.
                if not field_chars:
                    in_quotes = True
                else:
                    field_chars.append(ch)
            elif ch in ("\n", "\r"):
                # End of record (support CR, LF, and CRLF).
                if ch == "\r" and self._peek() == "\n":
                    self._read_char()  # consume '\n' in CRLF
                row.append("".join(field_chars))
                return row
            else:
                field_chars.append(ch)


class CustomCsvWriter:
    """
    CSV writer that handles quoting and escaping.

    This writer:
    - Writes comma-delimited CSV.
    - Quotes fields containing delimiters, quotes, or newlines.
    - Escapes internal quotes by doubling them.
    """

    def __init__(
        self,
        file_path: str,
        delimiter: str = ",",
        quotechar: str = '"',
        lineterminator: str = "\n",
        encoding: str = "utf-8",
    ) -> None:
        """
        Initialize the CSV writer.

        Args:
            file_path: Path to output CSV file.
            delimiter: Field delimiter character, default is comma.
            quotechar: Character used to quote fields, default is ".
            lineterminator: Line terminator string, default is "\n".
            encoding: File encoding, default is "utf-8".
        """
        if len(delimiter) != 1:
            raise ValueError("Delimiter must be a single character.")
        if len(quotechar) != 1:
            raise ValueError("Quote character must be a single character.")

        self.file_path = file_path
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.lineterminator = lineterminator
        self.encoding = encoding

        # Open file once and keep the handle for streaming writes.
        self._fh = open(self.file_path, "w", encoding=self.encoding, newline="")

    def __enter__(self) -> "CustomCsvWriter":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def close(self) -> None:
        """Close the underlying file."""
        if not self._fh.closed:
            self._fh.close()

    # ----------------------- Internal helpers -----------------------

    def _needs_quotes(self, field: str) -> bool:
        """
        Return True if the field must be quoted.

        A field is quoted if it contains:
        - the delimiter
        - the quotechar
        - a newline character
        """
        special_chars = (self.delimiter, self.quotechar, "\n", "\r")
        return any(c in field for c in special_chars)

    def _escape_field(self, field: str) -> str:
        """
        Return the field correctly quoted and with internal quotes escaped.

        If quoting is required, internal quote characters are doubled.
        """
        if self._needs_quotes(field):
            escaped = field.replace(self.quotechar, self.quotechar * 2)
            return f"{self.quotechar}{escaped}{self.quotechar}"
        return field

    # -------------------------- Public API --------------------------

    def writerow(self, row: Sequence[Union[str, int, float]]) -> None:
        """
        Write a single CSV row.

        Args:
            row: Sequence of fields; each field is converted to string.
        """
        processed: List[str] = []
        for field in row:
            s = str(field)
            processed.append(self._escape_field(s))
        line = self.delimiter.join(processed) + self.lineterminator
        self._fh.write(line)

    def writerows(self, rows: Sequence[Sequence[Union[str, int, float]]]) -> None:
        """
        Write multiple rows to the CSV file.

        Args:
            rows: Iterable/sequence of rows.
        """
        for row in rows:
            self.writerow(row)
