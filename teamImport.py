def teamCreation(string):
    pokemonDict = {}

    newList = string.split("\n\n")

    for x in range(1, len(newList)+1):
        pokemonDict[x] = {"pokemon": "",
                        "item": "",
                        "ability": "",
                        "tera": "",
                        "evs": "",
                        "nature": "",
                        "moves": "", 
                        "health": 100
        }
    z = 1
    for pokemon in newList:
        if "(F)" in pokemon:
            pokemon = pokemon.replace("(F)", "")
        elif "(M)" in pokemon:
            pokemon = pokemon.replace("(M)", "")
        itemIndex = pokemon.index("@")
        lineEnd = pokemon.index("\n")
        name = (pokemon[:itemIndex-1]).strip()
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

    return pokemonDict
