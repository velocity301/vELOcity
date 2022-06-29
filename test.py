import json
import random 

class Game:
    def __init__(self): 
        self.players = []
        self.team1 = []
        self.team2 = []
        self.map = random.choice(["Split", "Ascent", "Icebox", "Breeze", "Bind", "Haven", "Fracture", "Pearl"])

class Player:
    def __init__(self, username, ELO):
        self.username = username
        self.ELO = 1000
        self.wins = 0
        self.losses = 0
        self.kills = 0
        self.deaths = 0
        self.assists = 0

def writeJson(newData, fileName):
    with open(fileName,'r+') as f:
        fileData = json.load(f)
        print(fileData)
        fileData.append(newData.__dict__)
        f.seek(0)
        json.dump(fileData, f)

def checkJson(checkData, categoryOfData, fileName):
    with open(fileName, 'r+') as f:
        fileData = json.load(f)
        print(fileData)
        for elem in fileData:
            print(elem.get(categoryOfData))
            if (checkData == elem.get(categoryOfData)):
                return True
        return False

def addAttributeJson(newAttribute, newAttributeDefault, fileName):
    with open(fileName, 'r+') as f:
        fileData = json.load(f)
        for elem in fileData:
            print(elem)
            elem[newAttribute] = newAttributeDefault
        f.seek(0)
        json.dump(fileData, f)

def returnGameID():
    with open("config.json", 'r+') as f:
        fileData = json.load(f)
        print(fileData)
        return fileData["gameID"] 

def incrementGameID():
    with open("config.json", 'r+') as f:
        fileData = json.load(f)
        print(fileData)
        fileData["gameID"]+=1
        print(fileData)
        f.seek(0)
        json.dump(fileData, f)

def drawLobby():
    with open("games.json", 'r+') as f:
        lobbyString = ""
        fileData = json.load(f)
        




# print(checkJson("Alkminion", "username", "players.json"))

# addAttributeJson("losses", 0, "players.json")

# incrementGameID()
# print(returnGameID())

# writeJson(Game(), "games.json")