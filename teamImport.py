string = '''Garganacl @ Leftovers  
Ability: Purifying Salt  
Tera Type: Rock  
EVs: 252 HP / 252 SpD  
Bold Nature  
- Salt Cure  
- Protect  
- Rock Slide  
- Recover  

Garchomp @ Choice Scarf  
Ability: Rough Skin  
Tera Type: Dragon  
EVs: 252 Atk / 4 SpD / 252 Spe  
Jolly Nature  
- Earthquake  
- Dragon Claw  
- Liquidation  
- Poison Jab  

Kingambit @ Assault Vest  
Ability: Supreme Overlord  
Tera Type: Dark  
EVs: 252 HP / 252 Atk / 4 SpD  
Adamant Nature  
- Kowtow Cleave  
- Iron Head  
- Low Kick  
- Sucker Punch  

Ogerpon-Wellspring (F) @ Wellspring Mask  
Ability: Water Absorb  
Tera Type: Water  
EVs: 252 Atk / 4 SpD / 252 Spe  
Jolly Nature  
- Leech Seed  
- Ivy Cudgel  
- Knock Off  
- U-turn  

Zapdos @ Rocky Helmet  
Ability: Static  
Tera Type: Electric  
EVs: 248 HP / 252 SpA / 8 SpD  
Modest Nature  
IVs: 0 Atk  
- Roost  
- Thunderbolt  
- Heat Wave  
- Volt Switch  

Iron Valiant @ Booster Energy  
Ability: Quark Drive  
Tera Type: Fairy  
EVs: 252 Atk / 4 SpD / 252 Spe  
Jolly Nature  
- Close Combat  
- Ice Punch  
- Spirit Break  
- Psycho Cut  
'''

pokemonDict = {}

newList = string.split("\n\n")

for x in range(1, len(newList)+1):
    pokemonDict[x] = {"pokemon": "",
                      "item": "",
                      "ability": "",
                      "tera": "",
                      "evs": "",
                      "nature": "",
                      "moves": ""
    }
z = 1
for pokemon in newList:
    itemIndex = pokemon.index("@")
    lineEnd = pokemon.index("\n")
    name = pokemon[:itemIndex-1]
    item = (pokemon[itemIndex+1:lineEnd]).strip()

    abilityIndex = pokemon.index(":")
    lineEnd = pokemon.index("\n", abilityIndex)
    ability = (pokemon[abilityIndex+1:lineEnd]).strip()

    if "Tera" in pokemon:
        teraIndex = pokemon.index(":", lineEnd)
        lineEnd = pokemon.index("\n", teraIndex)
        tera = (pokemon[teraIndex+1:lineEnd]).strip()
    else:
        tera = None
    
    evIndex = pokemon.index(":", lineEnd)
    lineEnd = pokemon.index("\n", evIndex)
    evs = (pokemon[evIndex+1:lineEnd]).strip()
    evList = evs.split("/")
    fullEVsList = [0, 0, 0, 0, 0, 0]
    for stat in evList:
        if "HP" in stat:
            stat = stat.replace("HP", "")
            fullEVsList[0] = int(stat)
        elif "Atk" in stat:
            stat = stat.replace("Atk", "")
            fullEVsList[1] = int(stat)
        elif "Def" in stat:
            stat = stat.replace("Def", "")
            fullEVsList[2] = int(stat)
        elif "SpA" in stat:
            stat = stat.replace("SpA", "")
            fullEVsList[3] = int(stat)
        elif "SpD" in stat:
            stat = stat.replace("SpD", "")
            fullEVsList[4] = int(stat)
        elif "Spe" in stat:
            stat = stat.replace("Spe", "")
            fullEVsList[5] = int(stat)

    natureIndex = pokemon.index("Nature")
    secondLineEnd = pokemon.index("\n", natureIndex)
    nature = (pokemon[lineEnd+1:natureIndex]).strip()
    lineEnd = secondLineEnd

    moveString = pokemon[lineEnd+1:]
    moveList = moveString.split("\n")
    moveList = list(filter(None, moveList))
    for x in range(0, len(moveList)):
        moveString = moveList[x]
        moveString = (moveString.replace("-", "")).strip()
        moveList[x] = moveString

    pokemonDict[z]["pokemon"] = name
    pokemonDict[z]["item"] = item
    pokemonDict[z]["ability"] = ability
    pokemonDict[z]["tera"] = tera
    pokemonDict[z]["evs"] = fullEVsList
    pokemonDict[z]["nature"] = nature
    pokemonDict[z]["moves"] = moveList

    z+=1

print(pokemonDict)
