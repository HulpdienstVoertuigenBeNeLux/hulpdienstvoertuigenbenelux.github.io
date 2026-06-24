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
        return

    # Pak de lijst met rijen
    rows = data.get("values", data) if isinstance(data, dict) else data

    if not isinstance(rows, list):
        print("Fout: Geen rijen gevonden.")
        return

    # Filter: 
    # row[3] is TypeVoertuig
    # row[6] is Hulpdienst
    vehicle_types = []
    for row in rows[1:]:  # Sla header over
        if isinstance(row, list) and len(row) > 6:
            hulpdienst = str(row[6]).strip().lower()
            type_voertuig = str(row[3]).strip()
            
            # Alleen toevoegen als hulpdienst "brandweer" is
            if hulpdienst == "brandweer" and type_voertuig:
                vehicle_types.append(type_voertuig)
    
    counts = Counter(vehicle_types)
    
    with open('vehicle_counts.json', 'w', encoding='utf-8') as out_f:
        json.dump(dict(counts), out_f, indent=4, ensure_ascii=False)
    print("Statistieken voor Brandweer bijgewerkt.")

if __name__ == "__main__":
    process()
