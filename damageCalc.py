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
    base = ((((2*level/5)+2)*power*attack)/50)+2

    rolls = []
    for i in range(85, 101):
        rollMult = i /100.0
        dmg = math.floor(base/DEF) * modifiers * rollMult
        percent = (dmg/HP)*100
        rolls.append(round(percent, 1))
    
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
        return math.floor((2*base+iv+math.floor(ev/4))*level/100)+level+10
    else:
        return math.floor((math.floor((2*base+iv+math.floor(ev/4))*level/100)+5)*nature)

def loadPokedex():
    filePath = "pokedex.json"
    with open(filePath, "r") as f:
        return json.load(f)
    
def loadSmogon():
    filePath = "smogonData.json"
    with open(filePath, "r") as f:
        return json.load(f)
    
pokedex = loadPokedex()
smogon = loadSmogon()
target = "Iron-crown"

#hp, atk, def, spa, spd, spe
if target in pokedex:
    stats = pokedex[target]

target = "Iron Crown"
if target in smogon:
    sets = smogon[target]['spreads']
    sets = sets.keys()
    #sets is a list of "nature:0/0/0/0/0/0"

actualDefense = calculateStat(base=stats['def'], ev=0, iv=31, level=78, isHP=False)
print(f"Iron Crown's HP at lvl 78: {actualDefense}")



