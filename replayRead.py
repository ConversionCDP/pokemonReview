import json

with open("singlesBattle.json", "r") as f:
    data = json.load(f)

battleLog = data['log']

p1Team = []
p2Team = []
#get full team for both
if "clearpoke" in battleLog:
    teamsStart = battleLog.index("clearpoke")
    teamsEnd = battleLog.index("teampreview")
    fullTeams = battleLog[teamsStart+10:teamsEnd-2]
    teamList = fullTeams.split("\n")
    for poke in teamList:
        print(poke)
        if "p1" in poke:
            pokeStart = poke.index("p1|")
            pokeEnd = poke.index("|", pokeStart+3)
            pokemon = poke[pokeStart+3:pokeEnd]
            pokeList = pokemon.split(",")
            p1Team.append(pokeList)
        elif "p2" in poke:
            pokeStart = poke.index("p2|")
            pokeEnd = poke.index("|", pokeStart+3)
            pokemon = poke[pokeStart+3:pokeEnd]
            pokeList = pokemon.split(",")
            p2Team.append(pokeList)
    print(p1Team)
    print(p2Team)


#Get first mon in battle
if "switch" in battleLog:
    firstMonP1Index = battleLog.index("switch")
    p1MonEnd = battleLog.index("\n", firstMonP1Index)

    firstP1Mon = (battleLog[firstMonP1Index:p1MonEnd]).split("|")
    
    firstMonP2Index = battleLog.index("switch", p1MonEnd)
    p2MonEnd = battleLog.index("\n", firstMonP2Index)

    firstP2Mon = (battleLog[firstMonP2Index:p2MonEnd]).split("|")
    print(firstP1Mon)
    print(firstP2Mon)