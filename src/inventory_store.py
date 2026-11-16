"""Save working inventory without changing the original sample."""
import csv
import os
import tempfile
from pathlib import Path

from validate_data import DataError, REQUIRED_COLUMNS


def save_inventory(items, path):
    """Write a complete temporary CSV, then replace the working file."""
    path = Path(path)
    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            newline="",
            encoding="utf-8",
            dir=path.parent,
            suffix=".tmp",
            delete=False,
        ) as csv_file:
            temporary_path = Path(csv_file.name)

            writer = csv.DictWriter(
                csv_file,
                fieldnames=REQUIRED_COLUMNS,
                extrasaction="ignore",
            )
            writer.writeheader()
            writer.writerows(items)

        os.replace(temporary_path, path)

    except OSError as error:
        raise DataError(f"Could not save inventory: {error}") from error

    finally:
        if temporary_path is not None and temporary_path.exists():
            try:
                temporary_path.unlink()
            except OSError:
                pass
            