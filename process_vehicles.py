import json
import requests
import time

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
        except:
            time.sleep(5)
    return None

def process():
    # 1. Laad de sorteervolgorde uit Afkortingen.json
    try:
        with open('Afkortingen.json', 'r', encoding='utf-8') as f:
            sort_order_data = json.load(f)
            # Maak een map: {"Afkorting": Volgnummer}
            # Hiermee kunnen we supersnel opzoeken wat de positie is
            sort_map = {item['afkorting']: i for i, item in enumerate(sort_order_data)}
    except FileNotFoundError:
        print("Afkortingen.json niet gevonden, sorteervolgorde wordt standaard.")
        sort_map = {}

    # 2. Haal de voertuigdata op via de API
    data = get_data()
    if not data: return
    rows = data.get("values", data) if isinstance(data, dict) else data

    # 3. Tellen van de voertuigen
    counts = {}
    for row in rows[1:]:
        if isinstance(row, list) and len(row) > 6:
            hulpdienst = str(row[6]).strip().lower()
            afk = str(row[2]).strip()
            typ = str(row[3]).strip()
            
            # Filter: alleen Brandweer en volledige data
            if hulpdienst == "brandweer" and afk and typ:
                key = (afk, typ)
                counts[key] = counts.get(key, 0) + 1
    
    # 4. Sorteren op basis van de sort_map
    # Gebruik 999 voor voertuigen die niet in de lijst staan (komen onderaan)
    def sort_key(key):
        afk = key[0]
        return sort_map.get(afk, 999)

    sorted_keys = sorted(counts.keys(), key=sort_key)
    
    # 5. Resultaat opbouwen in de juiste volgorde
    result = []
    for key in sorted_keys:
        result.append({
            "afkorting": key[0], 
            "type": key[1], 
            "aantal": counts[key]
        })
    
    # 6. Wegschrijven naar JSON
    with open('vehicle_counts.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    process()
