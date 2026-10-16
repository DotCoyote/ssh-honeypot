import csv
import os
from pathlib import Path

from honeypot.sanitize import cleanup_text

def generate_csv_data(items: list[tuple[str, int]], category: str) -> list[tuple[str, str, int]]:
    return [(category, cleanup_text(item[0]), item[1]) for item in items]

def export_to_csv(logs: list, file_path: str) -> None:
    file = Path(file_path).resolve()
    file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file, 'w', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["category", "value", "count"])
        csv_writer.writerows(logs)
