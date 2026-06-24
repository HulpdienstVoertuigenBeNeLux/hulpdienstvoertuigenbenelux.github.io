import json
import requests
from collections import Counter

url = "https://hulpdienstvoertuigenbenelux.nl/fetch-sheet?region=NL"

def main():
    try:
        response = requests.get(url, timeout=30)
        data = response.json()
        
        # Sla header over (data[0]), verzamel "TypeVoertuig" (index 3)
        vehicle_types = [row[3] for row in data[1:] if len(row) > 3 and row[3]]
        counts = Counter(vehicle_types)
        
        # Opslaan in een bestand
        with open('vehicle_counts.json', 'w', encoding='utf-8') as f:
            json.dump(dict(counts), f, indent=4, ensure_ascii=False)
            
    except Exception as e:
        print(f"Fout bij ophalen data: {e}")

if __name__ == "__main__":
    main()
