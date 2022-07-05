# JSON Handling functions
import json
def objectToJson(object1):
    return json.dumps(object1.__dict__)

def writeJson(newData, fileName):
    with open(fileName,'r+') as f:
        fileData = json.load(f)
        fileData.append(newData.__dict__)
        f.seek(0)
        json.dump(fileData, f, indent = 4)

def checkJson(checkData, categoryOfData, fileName):
    with open(fileName, 'r+') as f:
        fileData = json.load(f)
        for elem in fileData:
            if (checkData == elem.get(categoryOfData)):
                return True
        return False
            
def addAttributeJson(newAttribute, newAttributeDefault, fileName):
    with open(fileName, 'r+') as f:
        fileData = json.load(f)
        for elem in fileData:
            elem[newAttribute] = newAttributeDefault
        f.seek(0)
        json.dump(fileData, f, indent = 4)

def incrementGameID():
    with open("config.json", 'r+') as f:
        fileData = json.load(f)
        fileData["gameID"]+=1
        f.seek(0)
        json.dump(fileData, f, indent = 4)

def decrementGameID():
    with open("config.json", 'r+') as f:
        fileData = json.load(f)
        fileData["gameID"]-=1
        f.seek(0)
        json.dump(fileData, f, indent = 4)

def returnGameID():
    with open("config.json", 'r+') as f:
        fileData = json.load(f)
        return fileData["gameID"] 

def addPlayerJson(playerName, team):
    with open("games.json", 'r+') as f:
        fileData = json.load(f)
        for elem in fileData: 
            if (elem["gameID"] == returnGameID()-1) and (playerName not in elem["players"]):
                if len(elem[team])<5:
                    elem["players"].append(playerName)
                    elem[team].append(playerName)
        f.seek(0)
        json.dump(fileData, f, indent = 4)

def removePlayerJson(playerName):
    with open("games.json", 'r+') as f:
        fileData = json.load(f)
    for elem in fileData:
        if (elem["gameID"] == returnGameID()-1):
            print("Found Game")
            if playerName in elem["players"]:
                print("player found, removing")
                elem["players"].remove(playerName)
            if playerName in elem["team1"]:
                elem["team1"].remove(playerName)
            if playerName in elem["team2"]:
                elem["team2"].remove(playerName)
    with open("games.json", 'w') as f:
        json.dump(fileData, f, indent = 4)

def drawLobby():
    lobbyString = "Map: "
    with open("games.json", 'r+') as f:
        fileData = json.load(f)
    for elem in fileData:
        if (elem["gameID"] == returnGameID()-1):
            lobbyString += elem["map"] + "              " + "game ID: " + str(elem["gameID"]) + "\n\n**Attackers**\n```"
            if len(elem["team1"]) == 0:
                lobbyString += "empty"
            else:
                lobbyString += "\n"
            for player in elem["team1"]:
                lobbyString += player + "\n"
            lobbyString += "```\n**Defenders**\n```"
            if len(elem["team2"]) == 0:
                lobbyString += "empty"
            else:
                lobbyString += "\n"
            for player in elem["team2"]:
                lobbyString += player + "\n"
            lobbyString += "```"
    print(lobbyString)
    return lobbyString

def getLobbyHeadCount():
    with open ("games.json", 'r+') as f:
        fileData = json.load(f)
    for elem in fileData:
        if (elem["gameID"] == returnGameID()-1):
            return len(elem["players"])

def setGameResult(result):
    with open("games.json", 'r+') as f:
        fileData = json.load(f)
    for elem in fileData:
        if (elem["gameID"] == returnGameID()-1):
            elem["result"] = result
    with open("games.json", 'w') as f:
        json.dump(fileData, f, indent = 4)

# def setWinELO(team, gameID):
#     with open("games.json", 'r+') as f:
#         gamesData = json.load(f)
#     for elem in gamesData:
#         if elem["gameID"] == gameID:
#             print("ELO test")
#             gameData = elem
#     print(gameData)
#     with open("players.json", 'r+') as f:
#         playersData = json.load(f)
    
