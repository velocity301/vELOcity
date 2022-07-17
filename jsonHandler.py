# JSON Handling functions
# TODO: rewrite Json handling functions to be faster (not have to loop through)
import json

def loadJson(fileName):
    with open(fileName, 'r+') as f:
        fileData = json.load(f)
    return fileData

def saveJson(fileData, fileName):
    with open(fileName, 'w') as f:
        json.dump(fileData, f, indent = 4)

def writeJson(newData, fileName):
    fileData = loadJson(fileName)
    fileData.append(newData.__dict__)
    saveJson(fileData, fileName)

def checkJson(checkData, categoryOfData, fileName):
    fileData = loadJson(fileName)
    for elem in fileData:
        if (checkData == elem.get(categoryOfData)):
            return True
    return False
            
def addAttributeJson(newAttribute, newAttributeDefault, fileName):
    fileData = loadJson(fileName)
    for elem in fileData:
        elem[newAttribute] = newAttributeDefault
    saveJson(fileData, fileName)

def incrementGameID():
    fileData = loadJson("config.json")
    fileData["gameID"]+=1
    saveJson(fileData, "config.json")

def decrementGameID():
    fileData = loadJson("config.json")
    fileData["gameID"]-=1
    saveJson(fileData, "config.json")

def returnGameID():
    fileData = loadJson("config.json")
    return fileData["gameID"] 

def addPlayerJson(playerName, team):
    removePlayerJson(playerName)
    fileData = loadJson("games.json")
    for elem in fileData: 
        if (elem["gameID"] == returnGameID()-1) and (playerName not in elem["players"]):
            if len(elem[team])<5:
                elem["players"].append(playerName)
                elem[team].append(playerName)    
    saveJson(fileData, "games.json")

def removePlayerJson(playerName):
    fileData = loadJson("games.json")
    for elem in fileData:
        if (elem["gameID"] == returnGameID()-1):
            if playerName in elem["players"]:
                elem["players"].remove(playerName)
            if playerName in elem["team1"]:
                elem["team1"].remove(playerName)
            if playerName in elem["team2"]:
                elem["team2"].remove(playerName)
    saveJson(fileData, "games.json")

def drawLobby():
    fileData = loadJson("games.json")
    lobbyString = "Map: "
    for elem in fileData:
        if (elem["gameID"] == returnGameID()-1):
            lobbyString += elem["map"] + "\n\n**Attackers**\n```"
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
    return lobbyString

def getLobbyHeadCount():
    fileData = loadJson("games.json")
    for elem in fileData:
        if (elem["gameID"] == returnGameID()-1):
            return len(elem["players"])

def setGameResult(result):
    fileData = loadJson("games.json")
    for elem in fileData:
        if (elem["gameID"] == returnGameID()-1):
            elem["result"] = result
    saveJson(fileData, "games.json")

def setWinELO(team, gameID):
    gamesData = loadJson("games.json")
    for elem in gamesData:
        if elem["gameID"] == gameID:
            gameData = elem
    playersData = loadJson("players.json")
    for member in gameData[team]:
        for player in playersData:
            if member == player["username"]:
                player["ELO"] += 10
    saveJson(playersData, "players.json")

def setLossELO(team, gameID):
    gamesData = loadJson("games.json")
    for elem in gamesData:
        if elem["gameID"] == gameID:
            gameData = elem
    playersData = loadJson("players.json")
    for member in gameData[team]:
        for player in playersData:
            if member == player["username"]:
                player["ELO"] -= 10
    saveJson(playersData, "players.json")

# returns a string for printing the current leaderboard    
def getPlayersSorted():
    playersList = []
    playersData = loadJson("players.json")
    for elem in playersData:
        playersList.append([elem["ELO"], elem["username"]])
    return sorted(playersList, reverse = True)

# deletes a player from the player list
def deletePlayer(discordName):
    playersData = loadJson("players.json")
    for elem in playersData:
        if elem["discordName"] == discordName:
            playersData.remove(elem)
    saveJson(playersData, "players.json")
