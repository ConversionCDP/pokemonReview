import json
from teamImport import teamCreation
from teamString import string
from damageCalc import loadPokedex, loadSmogon, loadMoves, calculateStat, calcPossibleByPercentage

#IF I MAKE A FUNCTION TO PULL THE POKEMON NAME FROM THE LINE AND HAVE IT RETURN IF IT IS P1 OR P2 THEN I CAN MAKE ALL OF THE "BIG REPLAY" FUNCTION SEPARATE FUNCTION CALLS THAT IS MUCH SMOOTHER
#MIGHT BE WORTH REWRITING ONCE THIS FUNCTIONS TO MAKE THE MAIN FUNCTION OTHER FUNCTION CALLS


pokedex = loadPokedex()
smogon = loadSmogon()
moves = loadMoves()

def loadTypeChart():
    filePath = "typeChart.json"
    with open(filePath, "r") as f:
        return json.load(f)
    
typeChart = loadTypeChart()

#Oppdictinary is team 1
#Userdictionary is team 2

def damageUpdate(player, playerDictionary, pokeName, sepTurn):
    healthIndex = sepTurn.index(player)
    healthStart = sepTurn.index("|", healthIndex)
    healthEnd = sepTurn.index("/", healthStart)
    newHealth = int(sepTurn[healthStart+1:healthEnd])

    playerDictionary[pokeName]["health"] = newHealth  
    return playerDictionary

def modifierSolve(userName, targetName, usedMove, item, ability, targetDictionary, moveUserDictionary):
    finalMod = 1
    if usedMove in moves:
        move = moves[usedMove]
    
    #Effectiveness Calculator
    tempTypes = targetDictionary[targetName]["activeType"]
    usedMoveType = move['type']
    for currType in tempTypes:
        if currType.capitalize() in typeChart["Defensive"]:
            currType = currType.capitalize()
            defTypeChart = typeChart["Defensive"]
            if usedMoveType in defTypeChart[currType]["Super"]:
                finalMod = finalMod*2.0
            elif usedMoveType in defTypeChart[currType]["Resist"]:
                finalMod = finalMod*0.5
            elif usedMoveType in defTypeChart[currType]["Immune"]:
                finalMod = 0
            else:
                finalMod = finalMod*1

    #STAB Calculator
    userTypes = moveUserDictionary[userName]["activeType"]
    activeTera = moveUserDictionary[userName]["teraActive"]
    for type in userTypes:
        if type.lower() == (move["type"]).lower() and activeTera == "Yes":
            finalMod = finalMod*2.0
        elif type.lower() == (move["type"]).lower():
            finalMod = finalMod*1.5
    
    if item:
        if item == "Life Orb":
            finalMod = finalMod*1.3
        elif item == "Choice Band" and move['category'] == "Physical":
            finalMod = finalMod*1.5
        elif item == "Choice Specs" and move['category'] == "Special":
            finalMod = finalMod*1.5  

    return finalMod

#NEED TO SOLVE MODIFIER CALCULATION TO NOT BE HARDCODED
#ALSO IF NO SETS ARE RETURNED AFTER SOLVE SET THEN DON'T REMOVE ALL "POSSIBLESETS". THIS COULD BE THE CASE FOR SOMETHING LIKE ASSAULT VEST ITEM
def solveDefSet(playerDictionary, pokeName, usedMove, percentageTaken, userAtk, trueMod):
    
    if usedMove in moves:
        move = moves[usedMove]

    possibleSet = []
    searchName = pokeName.lower()
    if searchName in pokedex:
        stats = pokedex[searchName]
    setList = playerDictionary[pokeName]["possibleSets"]

    for possible in setList:
        hp = calculateStat(base=stats['hp'], ev=int(possible[1][0]), iv=31, level=100, statName="hp", natureName=possible[0])
        if move['category'] == "Physical":
            defensiveStat = calculateStat(base=stats['def'], ev=int(possible[1][2]), iv=31, level=100, statName="def", natureName=possible[0])
        elif move['category'] == "Special":
            defensiveStat = calculateStat(base=stats['spd'], ev=int(possible[1][4]), iv=31, level=100, statName="spd", natureName=possible[0])

        low, high = calcPossibleByPercentage(100, userAtk, move['power'], hp, defensiveStat, trueMod)
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
        searchName = tempP1Team[0].lower()
        stats = pokedex[searchName]
        newStatList = []
        for statLine in stats:
            if str(statLine) in "hp, atk, def, spa, spd, spe":
                newStatList.append(stats[statLine])
        oppDictionary[tempP1Team[0]] = {"health": 100,
                                        "moves": set(),
                                        "possibleSets": [],
                                        "ability": [],
                                        "item": "",
                                        "tera": "",
                                        "teraActive": "No",
                                        "boosts": [0, 0, 0, 0, 0],
                                        "activeType": [],
                                        "status": [],
                                        "baseStats": newStatList}
    #Importing userDictionary to be used from teamImport
    tempUserDictionary = teamCreation(string)
    for poke in tempUserDictionary:
        newName = tempUserDictionary[poke]["pokemon"]
        searchName = newName.lower()
        stats = pokedex[searchName]
        newStatList = []
        for statLine in stats:
            if str(statLine) in "hp, atk, def, spa, spd, spe":
                newStatList.append(stats[statLine])
        userDictionary[newName] = {"health": 100,
                                           "moves": tempUserDictionary[poke]["moves"],
                                           "evs": tempUserDictionary[poke]["evs"],
                                           "ability": tempUserDictionary[poke]["ability"],
                                           "item": tempUserDictionary[poke]["item"],
                                           "boosts": [0, 0, 0, 0, 0],
                                           "tera": tempUserDictionary[poke]["tera"],
                                           "teraActive": "No",
                                           "nature": tempUserDictionary[poke]["nature"],
                                           "activeType": [],
                                           "status": [],
                                           "baseStats": newStatList}    
    
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
            '''for name in oppDictionary:
                print(f"oppDict: {name}")
            for name in userDictionary:
                print(f"UserDict: {name}")'''
            if "move" in sepTurn:
                p1Count = 0
                p2Count = 0
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
                        preHealth = oppDictionary[poke1Name]["health"]
                        oppDictionary = damageUpdate("p1a:", oppDictionary, poke1Name, sepTurn)
                    elif "p2a" in sepTurn:
                        userDictionary = damageUpdate("p2a:", userDictionary, poke2Name, sepTurn)
                elif "fnt" in sepTurn:
                    if "p1a" in sepTurn:
                        poke1Index = sepTurn.index("p1a:")
                        poke1Endex = sepTurn.index("|", poke1Index)
                        poke1Name = sepTurn[poke1Index+4:poke1Endex].strip()
                        oppDictionary[poke1Name]["status"] = ["fnt"]
                        oppDictionary[poke1Name]["health"] = 0
                    elif "p2a" in sepTurn:
                        poke2Index = sepTurn.index("p2a:")
                        poke2Endex = sepTurn.index("|", poke2Index)
                        poke2Name = sepTurn[poke2Index+4:poke2Endex].strip()
                        userDictionary[poke2Name]["status"] = ["fnt"]
                else:
                    if "p1a" in sepTurn:
                        preHealth = oppDictionary[poke1Name]["health"]
                        oppDictionary = damageUpdate("p1a:", oppDictionary, poke1Name, sepTurn)
                        postHealth = oppDictionary[poke1Name]["health"]
                        perTaken = (int(preHealth))-(int(postHealth))
                        if poke2Move in moves:
                            usedMove = moves[poke2Move]
                        if usedMove['category'] == "Physical":
                            userAttack = calculateStat(userDictionary[poke2Name]["baseStats"][1], userDictionary[poke2Name]["evs"][1], iv=31, level=100, statName="atk", natureName=userDictionary[poke2Name]["nature"])
                        elif usedMove['category'] == "Special":
                            userAttack = calculateStat(userDictionary[poke2Name]["baseStats"][3], userDictionary[poke2Name]["evs"][3], iv=31, level=100, statName="spa", natureName=userDictionary[poke2Name]["nature"])
                        modifier = modifierSolve(poke2Name, poke1Name, poke2Move, userDictionary[poke2Name]["item"], userDictionary[poke2Name]["ability"], oppDictionary, userDictionary)
                        oppDictionary = solveDefSet(oppDictionary, poke1Name, poke2Move, perTaken, userAttack, modifier)
                    elif "p2a" in sepTurn:
                        userDictionary = damageUpdate("p2a:", userDictionary, poke2Name, sepTurn)
            elif "-boost" in sepTurn:
                if "p1a" in sepTurn:
                    statIndex = sepTurn.index(poke1Name)
                    statEndex = sepTurn.index("|")
                    stat = (sepTurn[statEndex:]).split("|")
                    for z in range(0, 3):
                        stat.pop(0)
                    print(stat)
                    #I need to find out how they label all boosts since they are lower case
                    tempBoost = oppDictionary[poke1Name]["boosts"]
                    if stat[0] == "atk":
                        tempBoost[0] = tempBoost[0]+int(stat[1])
                    elif stat[0] == "def":
                        tempBoost[1] = tempBoost[1]+int(stat[1])
                    elif stat[0] == "spa":
                        tempBoost[2] = tempBoost[2]+int(stat[1])
                    elif stat[0] == "spd":
                        tempBoost[3] = tempBoost[3]+int(stat[1])
                    elif stat[0] == "spe":
                        tempBoost[4] = tempBoost[4]+int(stat[1])
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
                if "p1a" in sepTurn:
                    poke1Index = sepTurn.index("p1a:")
                    poke1Endex = sepTurn.index("|", poke1Index+1)
                    poke1Name = (sepTurn[poke1Index+4:poke1Endex]).strip()
                    newTeraType = [(sepTurn[poke1Endex+1:].strip()).lower()]
                    print(newTeraType)
                    oppDictionary[poke1Name]["activeType"] = newTeraType
                    oppDictionary[poke1Name]["tera"] = str(newTeraType[0])
                    oppDictionary[poke1Name]["teraActive"] = "Yes"
            elif "|switch|" in sepTurn:
                #keep track of active pokemon on field to determine "positioning" stats later for heuristic
                if "p1a" in sepTurn:
                    poke1Index = sepTurn.index("p1a:")
                    poke1Endex = sepTurn.index("|", poke1Index+1)
                    poke1Name = (sepTurn[poke1Index+4:poke1Endex]).strip()
                    print(f"Active Pokemon are now {poke1Name} and {poke2Name}")
                elif "p2a" in sepTurn:
                    poke2Index = sepTurn.index("p2a:")
                    poke2Endex = sepTurn.index("|", poke2Index+1)
                    poke2Name = (sepTurn[poke2Index+4:poke2Endex]).strip()
                    print(f"Active pokemon are now {poke1Name} and {poke2Name}")
            elif "|-status|" in sepTurn:
                if "p1a" in sepTurn:
                    poke1Index = sepTurn.index("p1a:")
                    poke1Endex = sepTurn.index("|", poke1Index+1)
                    poke1Name = (sepTurn[poke1Index+4:poke1Endex]).strip()
                    status = sepTurn[poke1Endex+1:].strip()
                    activeStatus = oppDictionary[poke1Name]["status"]
                    activeStatus.append(status)
                    oppDictionary[poke1Name]["status"] = activeStatus
                    print(oppDictionary[poke1Name]["status"])
                elif "p2a" in sepTurn:
                    poke2Index = sepTurn.index("p2a:")
                    poke2Endex = sepTurn.index("|", poke2Index+1)
                    poke2Name = (sepTurn[poke2Index+4:poke2Endex]).strip()
                    status = sepTurn[poke2Endex+1:].strip()
                    activeStatus = userDictionary[poke2Name]["status"]
                    activeStatus.append(status)
                    userDictionary[poke2Name]["status"] = activeStatus
                    print(userDictionary[poke2Name]["status"])
bigReplay()



    
    
