import requests
import json

#pulls data for a format from smogon
def smogonData(format_id="gen9ou"):
    url = f"https://pkmn.github.io/smogon/data/stats/{format_id}.json"
    data = requests.get(url).json()


    return data['pokemon']

fullList = smogonData(format_id="gen9ou")

with open("smogonData.json", "w") as f:
    json.dump(fullList, f, indent=2)
print("Done, saved successfully")