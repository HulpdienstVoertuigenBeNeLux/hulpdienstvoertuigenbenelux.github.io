import json
import requests

def process():
    url = "https://hulpdienstvoertuigenbenelux.nl/fetch-sheet?region=NL"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        data = response.json()
        rows = data.get("values", data) if isinstance(data, dict) else data
        
        # We maken een dictionary om te tellen met een unieke sleutel
        counts = {}
        for row in rows[1:]:
            if isinstance(row, list) and len(row) > 6:
                if str(row[6]).strip().lower() == "brandweer":
                    afkorting = str(row[2]).strip()
                    type_voertuig = str(row[3]).strip()
                    key = (afkorting, type_voertuig)
                    counts[key] = counts.get(key, 0) + 1
        
        # Omzetten naar de gewenste structuur: lijst van objecten
        result = []
        for (afk, typ), aantal in counts.items():
            result.append({
                "afkorting": afk,
                "type": typ,
                "aantal": aantal
            })
            
        with open('vehicle_counts.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=4, ensure_ascii=False)
            
    except Exception as e:
        print(f"Fout: {e}")

if __name__ == "__main__":
    process()
