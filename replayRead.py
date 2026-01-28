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

#Start Turn Stuff

oppDictionary = {}
#have user dictionary to keep up with health basically is the only thing it needs
userDictionary = {}

if "turn|1" in battleLog:
    turnStartIndex = battleLog.index("|turn|1")
    battleTurns = battleLog[turnStartIndex+1:]
    turnList = battleTurns.split("|turn|")

for turn in turnList:
    print(turnList)
    #Keep track of damage values of every pokemon at all times for opponent and user team. These values can easily be passed for math, heuristic, etc.
    '''Battle Dictionary = {
        pokemon1 = {
            health: 100/100,
            moves: [move1, move2, move3, move4],
            possibleSets: [set1, set2, set3, ...],
            ability: [ability],
            item: [item],
            }
    }'''

print(oppDictionary)
print(userDictionary)
