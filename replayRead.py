import json
from teamImport import teamCreation
from teamString import string
from damageCalc import loadPokedex, loadSmogon, loadMoves, calculateStat, calcPossibleByPercentage

pokedex = loadPokedex()
smogon = loadSmogon()
moves = loadMoves()

def damageUpdate(player, playerDictionary, pokeName, sepTurn):
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

def solveSet(playerDictionary, pokeName, usedMove, percentageTaken, userAtk):
    
    if usedMove in moves:
        move = moves[usedMove]

    possibleSet = []
    searchName = pokeName.lower()
    if searchName in pokedex:
        stats = pokedex[searchName]
    setList = playerDictionary[pokeName]["possibleSets"]

    for possible in setList:
        hp = calculateStat(base=stats['hp'], ev = int(possible[1][0]), iv=31, level=100, isHP=True, nature=1.0)
        if move['category'] == "Physical" and possible[0] in ("Bold", "Impish", "Lax", "Relaxed"):
            defensiveStat = calculateStat(base=stats['def'], ev=int(possible[1][2]), iv=31, level=100, isHP=False, nature = 1.1)
        elif move['category'] == "Physical" and possible[0] in ("Lonely", "Mild", "Gentle", "Hasty"):
            defensiveStat = calculateStat(base=stats['def'], ev=int(possible[1][2]), iv=31, level=100, isHP=False, nature=0.9)
        elif move['category'] == "Physical":
            defensiveStat = calculateStat(base=stats['def'], ev=int(possible[1][2]), iv=31, level=100, isHP=False, nature=1.0)
        elif move['category'] == "Special" and possible[0] in ("Calm", "Gentle", "Careful", "Sassy"):
            defensiveStat = calculateStat(base=stats['spd'], ev=int(possible[1][4]), iv=31, level=100, isHP=False, nature=1.1)
        elif move['category'] == "Special" and possible[0] in ("Naughty", "Lax", "Rash", "Naive"):
            defensiveStat = calculateStat(base=stats['spd'], ev=int(possible[1][4]), iv=31, level=100, isHP=False, nature=0.9)
        elif move['category'] == "Special":
            defensiveStat = calculateStat(base=stats['spd'], ev=int(possible[1][4]), iv=31, level=100, isHP=False, nature=1.0)
        
        
        low, high = calcPossibleByPercentage(100, userAtk, move['power'], hp, defensiveStat, modifiers=1.5)
        if low <= percentageTaken <= high:
            possibleSet.append(possible)

    playerDictionary[pokeName]["possibleSets"] = possibleSet
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
        oppDictionary[tempP1Team[0]] = {"health": 100,
                                        "moves": set(),
                                        "possibleSets": [],
                                        "ability": [],
                                        "item": "",
                                        "tera": "",
                                        "boosts": [0, 0, 0, 0, 0],
                                        "activeType": ""}
    #Importing userDictionary to be used from teamImport
    tempUserDictionary = teamCreation(string)
    for poke in tempUserDictionary:
        newName = tempUserDictionary[poke]["pokemon"]
        userDictionary[newName] = {"health": 100,
                                           "moves": tempUserDictionary[poke]["moves"],
                                           "evs": tempUserDictionary[poke]["evs"],
                                           "ability": tempUserDictionary[poke]["ability"],
                                           "item": tempUserDictionary[poke]["item"],
                                           "boosts": [0, 0, 0, 0, 0],
                                           "tera": tempUserDictionary[poke]["tera"],
                                           "nature": tempUserDictionary[poke]["nature"],
                                           "activeType": []}

    
    
    #oppTeam sets and active type set
    for pokeName in oppDictionary:
        setList = []
        searchName = pokeName.lower()
        newTypes = pokedex[searchName]["types"]
        oppDictionary[pokeName]["activeType"] = newTypes

        if pokeName in smogon:
            sets = smogon[pokeName]['spreads']
            sets = list(sets.keys())
        
        for x in range(0, len(sets)):
            setString = str(sets[x])
            colon = setString.index(":")
            nature = setString[:colon]
            EVs = setString[colon+1:]
            statList = EVs.split("/")
            tempList = [nature, statList]
            setList.append(tempList)
        
        oppDictionary[pokeName]["possibleSets"] = setList


    for pokeName in userDictionary:
        searchName = pokeName.lower()
        newTypes = pokedex[searchName]["types"]
        userDictionary[pokeName]["activeType"] = newTypes

    #Start Turn Stuff
    if "turn|1" in battleLog:
        turnStartIndex = battleLog.index("|turn|1")
        battleTurns = battleLog[turnStartIndex+1:]
        turnList = battleTurns.split("|turn|")

    #Go through and find Health Updates every turn

    for turn in turnList:
        splitTurns = turn.split("\n")
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
                        preHealth = oppDictionary[poke1Name]["health"]
                        oppDictionary = damageUpdate("p1a:", oppDictionary, poke1Name, sepTurn)
                        postHealth = oppDictionary[poke1Name]["health"]
                        perTaken = (int(preHealth))-(int(postHealth))
                        #So that you don't have to pass a static attack stat make sure to calc the attack sttat using the function with the attacking mon
                        oppDictionary = solveSet(oppDictionary, poke1Name, poke2Move, perTaken, userAtk=212)
                    elif "p2a" in sepTurn:
                        userDictionary = damageUpdate("p2a:", userDictionary, poke2Name, sepTurn)
            elif "-boost" in sepTurn:
                if "p1a" in sepTurn:
                    statIndex = sepTurn.index(poke1Name)
                    statEndex = sepTurn.index("|")
                    stat = (sepTurn[statEndex:]).split("|")
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
                    oppDictionary[poke1Name]["boosts"] == tempBoost
                    #make sure you do math, because the boosts probably only show the additive/negative instead of total
                else:
                    statIndex = sepTurn.index(poke2Name)
                    statEndex = sepTurn.index("|")
                    stat = (sepTurn[statEndex:]).split("|")
                    #update userDictionary after writing code to reformat
                    tempBoost = userDictionary
            elif "-terastallize" in sepTurn:
                #use this to keep track of a pokemon's current type, might also consider moves like conversion and burn up
                pass

bigReplay()



    
    
