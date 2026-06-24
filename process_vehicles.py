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
    data = get_data()
    if not data: return
    rows = data.get("values", data) if isinstance(data, dict) else data

    # Dictionary om te tellen: key is (afkorting, type), value is aantal
    counts = {}
    
    for row in rows[1:]:
        if isinstance(row, list) and len(row) > 6:
            # 6=Hulpdienst, 2=Afkorting, 3=TypeVoertuig
            if str(row[6]).strip().lower() == "brandweer":
                afk = str(row[2]).strip()
                typ = str(row[3]).strip()
                key = (afk, typ)
                counts[key] = counts.get(key, 0) + 1
    
    # Omzetten naar lijst voor de tabel
    result = []
    for (afk, typ), count in counts.items():
        result.append({"afkorting": afk, "type": typ, "aantal": count})
    
    with open('vehicle_counts.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    process()
