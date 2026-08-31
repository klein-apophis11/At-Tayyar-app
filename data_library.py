import json
import os

def load_prayer_data():
    base_path = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_path, 'prayer_text.json')

    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except IOError as e:
        print(f"Error loading offline data file: {e}")
        return {"JAFARI_STEPS": {}, "TASBIH_PHASES": []}

DATA = load_prayer_data()

# Securely extract the properties for your main script
JAFARI_STEPS = DATA.get("JAFARI_STEPS", {})
TASBIH_PHASES = DATA.get("TASBIH_PHASES", [])
