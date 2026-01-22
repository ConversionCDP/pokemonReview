import math

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

def calcPossibleByPercentage(level, attack, power, HP, DEF, modifiers=1.0):
    base = ((((2*level/5)+2)*power*attack)/50)+2

    rolls = []
    for i in range(85, 101):
        rollMult = i /100.0
        dmg = math.floor(base/DEF) * modifiers * rollMult
        percent = (dmg/HP)*100
        rolls.append(round(percent, 1))
    
    return min(rolls), max(rolls)

def finalHPCalc(percentageTaken, sets, rolls):
    for setName, (hp,d) in sets.items():
        low, high = calcPossibleByPercentage(100, 226, 120, hp, d, modifiers=1.5)
        if low <= percentageTaken <= high:
            print(f"Match Found: Opponent is likely running {setName}. Range: {low}% - {high}%")
        else:
            print(f"Set {setName} is impossible. Range: {low}% - {high}%")

sets = {
    "Offensive": (281, 206),
    "Bulky": (344, 230)
}

results = calcPossibleByDamage(level=75, power=65, attack=123, damageDealt=196, modifiers=6.0)

