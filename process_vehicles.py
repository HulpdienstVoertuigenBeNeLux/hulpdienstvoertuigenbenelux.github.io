import json
from collections import Counter
import os

def process():
    # Pad naar het gedownloade bestand
    file_path = 'raw_data.json'
    
    if not os.path.exists(file_path):
        print("Bestand raw_data.json niet gevonden!")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Verzamel "TypeVoertuig" (index 3)
    vehicle_types = [row[3] for row in data[1:] if len(row) > 3 and row[3]]
    counts = Counter(vehicle_types)
    
    # Sla resultaat op
    with open('vehicle_counts.json', 'w', encoding='utf-8') as f:
        json.dump(dict(counts), f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    process()
