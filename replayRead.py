import json
from teamImport import teamCreation
from teamString import string

def damageSend(player, playerDictionary, pokeName, sepTurn):
    healthIndex = sepTurn.index(player)
    healthStart = sepTurn.index("|", healthIndex)
    healthEnd = sepTurn.index("/", healthStart)
    newHealth = int(sepTurn[healthStart+1:healthEnd])
    if "p1a" in player:
        playerDictionary[pokeName]["health"] = newHealth
    else:
        for number in playerDictionary:
            if number['pokemon'] == pokeName:
                playerDictionary[number]['health'] == newHealth
    return playerDictionary

def bigReplay(fileName="singlesBattle.json", ):
    userDictionary = teamCreation(string)
    with open(fileName, "r") as f:
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


    #Get first mon in battle
    if "switch" in battleLog:
        firstMonP1Index = battleLog.index("switch")
        p1MonEnd = battleLog.index("\n", firstMonP1Index)

        firstP1Mon = (battleLog[firstMonP1Index:p1MonEnd]).split("|")
        
        firstMonP2Index = battleLog.index("switch", p1MonEnd)
        p2MonEnd = battleLog.index("\n", firstMonP2Index)

        firstP2Mon = (battleLog[firstMonP2Index:p2MonEnd]).split("|")

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
                                        "item": "",
                                        "boosts": [0, 0, 0, 0, 0],
                                        "activeType": ""}
    #Importing userDictionary to be used from teamImport
    #REFORMAT THIS TO MATCH CLOSER TO OPPDICTIONARY, IE INCLUDE FULL LIST BUT DON'T START WITH 1,2,3 ETC.
    userDictionary = teamCreation(string)
    for poke in userDictionary:
        userDictionary[poke]["boosts"] = [0, 0, 0, 0, 0]

    #Start Turn Stuff
    if "turn|1" in battleLog:
        turnStartIndex = battleLog.index("|turn|1")
        battleTurns = battleLog[turnStartIndex+1:]
        turnList = battleTurns.split("|turn|")

    #Go through and find Health Updates every turn

    for turn in turnList:
        splitTurns = turn.split("\n")
        print(turn)
        for sepTurn in splitTurns:
            print(sepTurn)
            if "move" in sepTurn:
                p1Count = sepTurn.count("p1a")
                p2Count = sepTurn.count("p2a")
                if p1Count == 1 and p2Count == 1:
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
                elif p1Count > p2Count:
                    #find p1 used move which target itself
                    poke1Index = sepTurn.index("p1a:")
                    poke1Endex = sepTurn.index("|", poke1Index)
                    poke1Name = (sepTurn[poke1Index+4:poke1Endex]).strip()
                    poke1Move = (sepTurn[poke1Endex+1:(sepTurn.index("|", poke1Endex+1))])
                    tempMoves = oppDictionary[poke1Name]["moves"]
                    tempMoves.add(poke1Move)
                    oppDictionary[poke1Name]["moves"] = tempMoves
                else:
                    poke2Index = sepTurn.index("p2a:")
                    poke2Endex = sepTurn.index("|", poke2Index)
                    poke2Name = (sepTurn[poke2Index+4:poke2Endex]).strip()
                    poke2Move = (sepTurn[poke2Endex+1:(sepTurn.index("|", poke2Endex+1))])
            elif "-damage" in sepTurn:
                if "[from]" in sepTurn:
                    if "p1a" in sepTurn:
                        pass
                else:
                    if "p1a" in sepTurn:
                        oppDictionary = damageSend("p1a:", oppDictionary, poke1Name, sepTurn)
                        print(oppDictionary)
                        #Once you have the dictionary for health updated, need to call damage functions
                        #Also need to call functions to get data then pass all data to damage functions to find potential sets
                        #Return potential sets and update dictionary
                    elif "p2a" in sepTurn:
                        userDictionary = damageSend("p2a:", userDictionary, poke2Name, sepTurn)
                        print(userDictionary)
            elif "-boost" in sepTurn:
                if "p1a" in sepTurn:
                    statIndex = sepTurn.index(poke1Name)
                    statEndex = sepTurn.index("|")
                    stat = (sepTurn[statEndex:]).split("|")
                    print(stat)
                    #I need to find out how they label all boosts since they are lower case
                    tempBoost = oppDictionary[poke1Name]["boosts"]
                    if stat[0] == "atk":
                        tempBoost[0] == tempBoost[0]+stat[1]
                    elif stat[0] == "def":
                        tempBoost[1] == tempBoost[1]+stat[1]
                    elif stat[0] == "spa":
                        tempBoost[2] == tempBoost[2]+stat[1]
                    elif stat[0] == "spd":
                        tempBoost[3] == tempBoost[3]+stat[1]
                    elif stat[0] == "spe":
                        tempBoost[4] == tempBoost[4]+stat[1]
                    print(tempBoost)
                    oppDictionary[poke1Name]["boosts"] == tempBoost
                    #make sure you do math, because the boosts probably only show the additive/negative instead of total
                else:
                    statIndex = sepTurn.index(poke2Name)
                    statEndex = sepTurn.index("|")
                    stat = (sepTurn[statEndex:]).split("|")
                    print(stat)
                    #update userDictionary after writing code to reformat
                    tempBoost = userDictionary
            elif "-terastallize" in sepTurn:
                #use this to keep track of a pokemon's current type, might also consider moves like conversion and burn up
                pass

bigReplay()



    
    
