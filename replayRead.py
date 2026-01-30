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

oppDictionary = {}
#have user dictionary to keep up with health basically is the only thing it needs
userDictionary = {}

for x in range(0, len(p1Team)):
    tempP1Team = p1Team[x]
    tempP2Team = p2Team[x]
    oppDictionary[tempP1Team[0]] = {"health": 100,
                                    "moves": set(),
                                    "possibleSets": [],
                                    "ability": [],
                                    "item": ""}
    userDictionary[tempP2Team[0]] = {"health": 100,
                                     "moves": set(),
                                     "possibleSets": [],
                                     "ability": [],
                                     "item": ""}

#Start Turn Stuff
if "turn|1" in battleLog:
    turnStartIndex = battleLog.index("|turn|1")
    battleTurns = battleLog[turnStartIndex+1:]
    turnList = battleTurns.split("|turn|")

for turn in turnList:
    splitTurns = turn.split("\n")
    print(turn)
    for sepTurn in splitTurns:
        print(sepTurn)
        if "move" in sepTurn:
            poke1Index = sepTurn.index("p1a:")
            poke2Index = sepTurn.index("p2a:")
            if poke1Index < poke2Index:
                poke1Endex = sepTurn.index("|", poke1Index)
                poke1Name =  (sepTurn[poke1Index+4:poke1Endex]).strip()
                poke1Move = (sepTurn[poke1Endex+1:(sepTurn.index("|", poke1Endex+1))])
                tempMoves = oppDictionary[poke1Name]["moves"]
                tempMoves.add(poke1Move)
                oppDictionary[poke1Name]["moves"] = tempMoves
                if "[miss]" in sepTurn:
                    poke2Endex = sepTurn.index("|", poke2Index)
                    poke2Name = (sepTurn[poke2Index+4:poke2Endex]).strip()
                else:
                    poke2Name = (sepTurn[poke2Index+4:]).strip()
                    print(poke2Name)
            else:
                poke2Endex = sepTurn.index("|", poke2Index)
                poke2Name = (sepTurn[poke2Index+4:poke2Endex]).strip()
                poke2Move = (sepTurn[poke2Endex+1:(sepTurn.index("|", poke2Endex+1))])
                #don't add move to dictionary because I should already know moves
                if "[miss]" in sepTurn:
                    poke1Endex = sepTurn.index("|", poke1Index)
                    poke1Name = (sepTurn[poke1Index+4:poke1Endex]).strip()
                else:
                    poke1Name = (sepTurn[poke1Index+4:]).strip()
                    print(poke1Name)
        elif "-damage" in sepTurn:
            if "p1a" in sepTurn:
                healthIndex = sepTurn.index("p1a:")
                healthStart = sepTurn.index("|", healthIndex)
                healthEnd = sepTurn.index("/", healthStart)
                newHealth = int(sepTurn[healthStart+1:healthEnd])
                print(newHealth)
                oppDictionary[poke1Name]["health"] = newHealth
                print(oppDictionary[poke1Name])
            elif "p2a" in sepTurn:
                healthIndex = sepTurn.index("p2a:")
                healthStart = sepTurn.index("|", healthIndex)
                healthEnd = sepTurn.index("/", healthStart)
                newHealth = int(sepTurn[healthStart+1:healthEnd])
                print(newHealth)
                userDictionary[poke2Name]["health"] = newHealth
                print(userDictionary[poke2Name])

    
    
