import json
import requests
import time
from collections import Counter

def get_data():
    url = "https://hulpdienstvoertuigenbenelux.nl/fetch-sheet?region=NL"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Referer": "https://hulpdienstvoertuigenbenelux.nl/"
    }
    # Probeer verbinding te maken met retry-logica
    for i in range(3):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Poging {i+1} mislukt: {e}")
            time.sleep(5)
    return None

def process():
    data = get_data()
    if not data:
        print("Kon data niet ophalen.")
        return

    # Sla header over en pak "TypeVoertuig" (index 3)
    vehicle_types = [row[3] for row in data[1:] if len(row) > 3 and row[3]]
    counts = Counter(vehicle_types)
    
    with open('vehicle_counts.json', 'w', encoding='utf-8') as out_f:
        json.dump(dict(counts), out_f, indent=4, ensure_ascii=False)
    print("vehicle_counts.json succesvol bijgewerkt.")

if __name__ == "__main__":
    process()
