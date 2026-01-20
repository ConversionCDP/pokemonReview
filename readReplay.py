import json

file = "battle.json"

def loadReplay(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)

    inputLog = data.get('inputlog', "")
    lines = inputLog.split("\n")

    playerInfo = {}
    battleSeed = None
    actions = []


    for line in lines:
        if line.startswith(">start"):
            startData = json.loads(line.split(' ', 1)[1])
            battleSeed = startData.get('seed')
        elif line.startswith(">player"):
            parts = line.split(' ', 2)
            pID = parts[1]
            pData = json.loads(parts[2])
            playerInfo[pID] = pData.get('name')
        elif line.startswith(">p1") or line.startswith(">p2"):
            actions.append(line)

    return {
        "seed": battleSeed,
        "p1Name": playerInfo.get('p1'),
        "p2Name": playerInfo.get('p2'),
        "actions": actions
    }

battleData = loadReplay("battle.json")
print(f"Reviewing Battle: {battleData['p1Name']} vs {battleData['p2Name']}")
print(f"Battle Seed: {battleData['seed']}")
print(f"First 3 actions: {battleData['actions'][:3]}")

