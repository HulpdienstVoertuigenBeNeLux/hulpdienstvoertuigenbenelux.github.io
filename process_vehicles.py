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
    if data is None: return

    rows = data.get("values", data) if isinstance(data, dict) else data
    if not isinstance(rows, list): return

    stats = {}
    for row in rows[1:]:
        if isinstance(row, list) and len(row) > 6:
            hulpdienst = str(row[6]).strip().lower()
            type_voertuig = str(row[3]).strip()
            afkorting = str(row[4]).strip()
            
            if hulpdienst == "brandweer" and type_voertuig:
                # Combineer type en afkorting
                key = f"{type_voertuig} ({afkorting})"
                stats[key] = stats.get(key, 0) + 1
    
    with open('vehicle_counts.json', 'w', encoding='utf-8') as out_f:
        json.dump(stats, out_f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    process()
