import json
import requests
import time
from collections import Counter

def get_data():
    url = "https://hulpdienstvoertuigenbenelux.nl/fetch-sheet?region=NL"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Referer": "https://hulpdienstvoertuigenbenelux.nl/",
        "Accept": "application/json"
    }
    
    # Retry logica voor betrouwbaarheid
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
    
    if data is None:
        print("Fout: Geen data ontvangen van de server.")
        return

    # Bepaal waar de lijst met rijen staat (hanteert lijst of dict met 'values')
    if isinstance(data, dict):
        rows = data.get("values", [])
    elif isinstance(data, list):
        rows = data
    else:
        print(f"Onbekend JSON formaat: {type(data)}")
        return

    if not rows or not isinstance(rows, list):
        print("Fout: Geen rijen gevonden in de data.")
        return

    # Sla header over (row 0) en tel "TypeVoertuig" (index 3)
    # We controleren of de rij een lijst is en minimaal 4 elementen bevat
    vehicle_types = [
        row[3] for row in rows[1:] 
        if isinstance(row, list) and len(row) > 3 and row[3]
    ]
    
    counts = Counter(vehicle_types)
    
    # Sla resultaat op
    try:
        with open('vehicle_counts.json', 'w', encoding='utf-8') as out_f:
            json.dump(dict(counts), out_f, indent=4, ensure_ascii=False)
        print("vehicle_counts.json succesvol bijgewerkt.")
    except Exception as e:
        print(f"Fout bij schrijven bestand: {e}")

if __name__ == "__main__":
    process()
