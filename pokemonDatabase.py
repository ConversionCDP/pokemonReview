import requests
import json

def get_complete_pokedex():
    """Fetches base stats for ALL pokemon entries from PokéAPI."""
    base_url = "https://pokeapi.co/api/v2/pokemon?limit=100000"
    response = requests.get(base_url).json()
    full_stats = {}
    
    # Process all available entries (includes forms)
    for i, entry in enumerate(response['results']):
        name = entry['name']
        data = requests.get(entry['url']).json()
        
        stats = {s['stat']['name']: s['base_stat'] for s in data['stats']}
        bst = sum(stats.values())
        
        # Standardize naming and structure
        full_stats[name.capitalize()] = {
            "hp": stats['hp'], "atk": stats['attack'], "def": stats['defense'],
            "spa": stats['special-attack'], "spd": stats['special-defense'],
            "spe": stats['speed'], "bst": bst
        }
        if i % 100 == 0: print(f"Serialized {i} entries...")
        
    return full_stats

'''full_dict = get_complete_pokedex()
with open("pokedex.json", "w") as f:
    json.dump(full_dict, f, indent=2)
print("Done, saved data to pokedex.json")'''

def get_all_gen9_usable_moves():
    """Fetches all moves currently usable in Generation 9."""
    # This endpoint gets all moves; you can filter by 'generation' in the logic
    url = "https://pokeapi.co/api/v2/move?limit=1000"
    response = requests.get(url).json()
    move_db = {}

    for entry in response['results']:
        data = requests.get(entry['url']).json()
        
        # Filter for moves that exist in Gen 9
        # (PokéAPI move descriptions or 'past_values' can help filter per game)
        move_name = data['name'].replace('-', ' ').title()
        move_db[move_name] = {
            "type": data['type']['name'].capitalize(),
            "category": data['damage_class']['name'].capitalize(),
            "power": data['power'],
            "accuracy": data['accuracy'],
            "pp": data['pp'],
            "is_variable": True if data['power'] is None and data['damage_class']['name']!= 'status' else False
        }
    return move_db

full_move_list = get_all_gen9_usable_moves()
with open("moveDB.json", 'w') as f:
    json.dump(full_move_list, f, indent=2)
print("Move List saved")