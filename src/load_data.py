"""Read an inventory CSV file from disk and report file problems clearly."""
import csv
import os

from validate_data import DataError


def read_csv_rows(path):
    """Return (column_names, rows) for the CSV file at `path`.

    Every row is a dictionary keyed by column name. File problems are turned
    into DataError with a message a non-programmer can act on.
    """
    path = os.fspath(path)
    try:
        # utf-8-sig quietly removes the invisible marker Excel sometimes adds.
        with open(path, newline="", encoding="utf-8-sig") as csv_file:
            reader = csv.DictReader(csv_file, strict=True)
            if not reader.fieldnames:
                raise DataError("The file '" + path + "' is empty.")
            # Ignore capital letters and stray spaces in the header row.
            reader.fieldnames = [name.strip().lower() for name in reader.fieldnames]
            column_names = reader.fieldnames
            rows = []
            for row in reader:
                row['__line_number__'] = reader.line_num
                rows.append(row)
    except FileNotFoundError:
        raise DataError("File not found: '" + path + "'. Check the name and folder.")
    except IsADirectoryError:
        raise DataError("'" + path + "' is a folder, not a CSV file.")
    except PermissionError:
        raise DataError("Not allowed to read '" + path + "'. Is it open or protected?")
    except UnicodeDecodeError:
        raise DataError("'" + path + "' does not look like a text CSV file.")
    except csv.Error as error:
        raise DataError("'" + path + "' is not a valid CSV file: " + str(error))
    except OSError as error:
        raise DataError("Could not read '" + path + "': " + str(error))

    return column_names, rows
