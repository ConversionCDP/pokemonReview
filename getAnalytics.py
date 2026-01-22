import requests

def likelyItem(pokemon, format_id="gen9ou"):
    url = f"https://pkmn.github.io/smogon/data/stats/{format_id}.json"
    data = requests.get(url).json()

    items = data['pokemon'][pokemon]['items']
    print(items)

    print(data['pokemon'][pokemon])

    return list(items.keys())[0]

item = likelyItem("Garchomp")
print(item)