import json
from collections import Counter
import os

def process():
    file_path = 'raw_data.json'
    
    if not os.path.exists(file_path):
        print(f"Fout: {file_path} niet gevonden.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            # Sla de header (index 0) over en pak index 3 (TypeVoertuig)
            vehicle_types = [row[3] for row in data[1:] if len(row) > 3 and row[3]]
            counts = Counter(vehicle_types)
            
            with open('vehicle_counts.json', 'w', encoding='utf-8') as out_f:
                json.dump(dict(counts), out_f, indent=4, ensure_ascii=False)
            print("vehicle_counts.json succesvol bijgewerkt.")
        except Exception as e:
            print(f"Fout bij verwerken JSON: {e}")

if __name__ == "__main__":
    process()
