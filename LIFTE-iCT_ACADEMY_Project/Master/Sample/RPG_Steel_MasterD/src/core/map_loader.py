import csv
from pathlib import Path
def load_csv_map(path):
    p = Path(path)
    if not p.exists(): raise ValueError(f"Map not found: {path}")
    with p.open(encoding='utf-8') as f:
        return [[int(c) for c in row] for row in csv.reader(f)]