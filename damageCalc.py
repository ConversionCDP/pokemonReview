import math
import json

#Calcs possible defense stat using damage dealt in actual HP
def calcPossibleByDamage(level, power, attack, damageDealt, modifiers=1.0):
    possibleDefense = []
    baseDamage = ((2*level)/5)+2
    baseDamage = (baseDamage * power * attack)/50

    for d in range(1, 601):
        maxDamage = ((baseDamage/d) + 2) * modifiers * 1.0
        minDamage = ((baseDamage/d) + 2) * modifiers * 0.85

        if minDamage <= damageDealt <= maxDamage:
            possibleDefense.append(d)

    if possibleDefense:
        print(f"Possible stat: {min(possibleDefense)} to {max(possibleDefense)}")
    else:
        print("No possible stat found")
        
    return possibleDefense

#First step to calc possible HP and DEF stats using percentage of damage dealt
def calcPossibleByPercentage(level, attack, power, HP, DEF, modifiers=1.0):
    rolls = []
    
    levelFactor = (2*level // 5) + 2
    baseDamage = (levelFactor * power * attack // DEF)
    baseDamage = (baseDamage // 50)+2
    for i in range(85, 101):
        damageAtRoll = (baseDamage * i) //100
        finalDamage = int(damageAtRoll * modifiers)
        percent = math.floor(finalDamage * 1000 / HP) / 10
        rolls.append(percent)
    
    return min(rolls), max(rolls)

#Final step to calc set using percentage of damage dealt
def finalHPCalc(percentageTaken, sets):
    for setName, (hp,d) in sets.items():
        low, high = calcPossibleByPercentage(100, 226, 120, hp, d, modifiers=1.5)
        if low <= percentageTaken <= high:
            print(f"Match Found: Opponent is likely running {setName}. Range: {low}% - {high}%")
        else:
            print(f"Set {setName} is impossible. Range: {low}% - {high}%")

#Calculate Stats
def calculateStat(base, ev, iv=31, level=100, isHP=False, nature=1.0):
    if isHP:
        return ((2*base+iv+(ev//4))*level//100)+level+10
    else:
        stat = ((2*base+iv+(ev//4))*level//100)+5
        return math.floor(stat*nature)
    
def loadPokedex():
    filePath = "pokedex.json"
    with open(filePath, "r") as f:
        return json.load(f)
    
def loadSmogon():
    filePath = "smogonData.json"
    with open(filePath, "r") as f:
        return json.load(f)
    
def loadMoves():
    filePath = "moveDB.json"
    with open(filePath, 'r') as f:
        return json.load(f)
    
pokedex = loadPokedex()
smogon = loadSmogon()
moves = loadMoves()

attack = 182
possibleSet = []
percentageTaken = 31
target = "Suicune"
usedMove = "Earthquake"
if usedMove in moves:
    move = moves[usedMove]
    print(move)

target = target.lower()
#hp, atk, def, spa, spd, spe
if target in pokedex:
    stats = pokedex[target]

target = "Suicune"
if target in smogon:
    sets = smogon[target]['spreads']
    sets = list(sets.keys())
    #sets is a list of "nature:0/0/0/0/0/0"

setList = []
for x in range(0, len(sets)):
    set = str(sets[x])
    colon = set.index(":")
    nature = set[:colon]
    EVs = set[colon+1:]
    statList = EVs.split("/")
    tempList = [nature, statList]
    setList.append(tempList)
    

for set in setList:
    hp = calculateStat(base=stats['hp'], ev = int(set[1][0]), iv=31, level=50, isHP=True, nature=1.0)
    print(set[1])
    if move['category'] == "Physical" and set[0] in ("Bold", "Impish", "Lax", "Relaxed"):
        defensiveStat = calculateStat(base=stats['def'], ev=int(set[1][2]), iv=31, level=50, isHP=False, nature = 1.1)
    elif move['category'] == "Physical" and set[0] in ("Lonely", "Mild", "Gentle", "Hasty"):
        defensiveStat = calculateStat(base=stats['def'], ev=int(set[1][2]), iv=31, level=50, isHP=False, nature=0.9)
    elif move['category'] == "Physical":
        defensiveStat = calculateStat(base=stats['def'], ev=int(set[1][2]), iv=31, level=50, isHP=False, nature=1.0)
    elif move['category'] == "Special" and set[0] in ("Calm", "Gentle", "Careful", "Sassy"):
        defensiveStat = calculateStat(base=stats['spd'], ev=int(set[1][4]), iv=31, level=50, isHP=False, nature=1.1)
    elif move['category'] == "Special" and set[0] in ("Naughty", "Lax", "Rash", "Naive"):
        defensiveStat = calculateStat(base=stats['spd'], ev=int(set[1][4]), iv=31, level=50, isHP=False, nature=0.9)
    elif move['category'] == "Special":
        defensiveStat = calculateStat(base=stats['spd'], ev=int(set[1][4]), iv=31, level=50, isHP=False, nature=1.0)
    
    
    low, high = calcPossibleByPercentage(50, 182, move['power'], hp, defensiveStat, modifiers=1.5)
    if low <= percentageTaken <= high:
        possibleSet.append(set)

    print(possibleSet)

#actualDefense = calculateStat(base=stats['def'], ev=0, iv=31, level=78, isHP=False)
#print(f"Iron Crown's HP at lvl 78: {actualDefense}")



