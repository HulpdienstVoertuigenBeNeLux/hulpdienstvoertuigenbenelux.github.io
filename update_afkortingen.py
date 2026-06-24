import pandas as pd
import json
import os

def update_afkortingen():
    # Haal de URL uit de GitHub Secret omgeving
    url = os.environ.get('SHEET_URL')
    
    if not url:
        print("Fout: SHEET_URL secret niet gevonden!")
        return

    df = pd.read_csv(url, usecols=[0, 1])
    df.columns = ['afkorting', 'type']
    df = df.dropna().drop_duplicates()
    
    data = df.to_dict(orient='records')
    with open('Afkortingen.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    update_afkortingen()
