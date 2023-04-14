import pymongo
from pymongo import MongoClient
import json
import dns.resolver
from jsonHandler import *
import pprint
import random

dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8'] # this is a google public dns server,  use whatever dns server you like here
client = pymongo.MongoClient("mongodb+srv://velocity300:vELOcity300@elo.r5j0e.mongodb.net/?retryWrites=true&w=majority&ssl=true")
db = client.vELOcity

class Player:
    def __init__(self, username, valorantName, discordName, guildID):
        self.discordName = discordName
        self.valorantName = valorantName
        self.guildInfo = [{"guildID": guildID, "ELO": 1000, "username": username}]
class Game:
    def __init__(self, gameID, guildID): 
        self.players = []
        self.team1 = []
        self.team2 = []
        self.map = random.choice(["Split", "Ascent", "Icebox", "Breeze", "Bind", "Haven", "Fracture", "Pearl"])
        self.gameID = gameID
        self.result = "waiting to start"
        self.guild = guildID

# checks if user exists in players collection
def checkUser(discordName):
    target = db["players"]
    query = {"discordName": discordName}
    if target.count_documents(query) == 1:
        return True
    else: 
        return False

# is discordName registered in the server guildID
def checkGuild(discordName, guildID):
    if checkUser(discordName) == False:
        return False
    target = db["players"]
    query = {"discordName": discordName}
    result = target.find(query, {"guildInfo": 1, "_id": 0})
    for elem in result:
        for guild in elem["guildInfo"]:
            if guild["guildID"] == str(guildID):
                return True
    return False
# add a player to a new guild when they are already registered in one or more other guilds
def addPlayerWithExistingGuild(discordName, guildID, username):
    target = db["players"]
    query = {"discordName": discordName}
    newGuildInfo  = {'guildID': str(guildID), 'ELO': 1000, 'username': username}
    result = target.update_one(query, {"$push": {"guildInfo": newGuildInfo}})

# adds a document (dictionary) to a collection (collectionName)
def addDocument(dictionary, collectionName):
    target = db[collectionName]
    result = target.insert_one(dictionary)

# adds a list of documents (dictionaries) to a collection (collectionName)
def addDocuments(dictionaries, collectionName):
    target = db[collectionName]
    result = target.insert_many(dictionaries)

# removes a document that has a field (key) with value (value) from a collection (collectionName)
def removeDocument(key, value, collectionName):
    target = db[collectionName]
    query = {key:value}
    result = target.delete_one(query)

# counts how many documents in a collection (collectionName) there are 
# with a field (key) and value (value)
def countInstances(key, value, collectionName):
    target = db[collectionName]
    query = {key:value}
    return target.count_documents(query)

def getCurrentLobbyStatus(guildID):
    target = db["config"]
    query = {"guildID": guildID}
    return target.find_one(query, {"currentLobby": 1, "_id": 0})["currentLobby"]

def setCurrentLobbyStatus(guildID, status): 
    target = db["config"] 
    query = {"guildID": guildID}
    newValue = { "$set": { "currentLobby": status}}
    result = target.update_one(query, newValue)

def getCurrentGameID(guildID):
    target = db["config"]
    query = {"guildID": guildID}
    return target.find_one(query, {"gameID": 1, "_id": 0})["gameID"]

def incrementGameID(guildID):
    target = db["config"]
    query = {"guildID": guildID}
    newValue = {"$inc": { "gameID": 1}}
    result = target.update_one(query, newValue)

def createGame(gameObject): 
    addDocument(gameObject, "games")

def getLobbyHeadCount(guildID, gameID):
    target = db["games"]
    query = {"guildID": guildID, "gameID": gameID}
    result = target.find_one(query, {"players": 1, "_id": 0})
    # print(result["players"])
    return len(result["players"])

def drawLobby(guildID, gameID):
    target = db["games"]
    query = {"guildID": guildID, "gameID": gameID}
    result = target.find_one(query, {"_id": 0})
    # print(result["players"])
    lobbyString = "Map: " + result["map"] + "\n**Attackers**\n```\n" 
    if len(result["team1"]) == 0:
        lobbyString += "empty"
    for elem in result["team1"]:
        lobbyString += elem.split('#')[0] +"\n"
    lobbyString += "```\n**Defenders**\n```\n"
    if len(result["team2"]) == 0:
        lobbyString += "empty"
    for elem in result["team2"]:
        lobbyString += elem.split('#')[0] +"\n"
    lobbyString += "```"
    #     if (elem["gameID"] == returnGameID()-1):
    #         lobbyString += elem["map"] + "\n\n**Attackers**\n```"
    #         if len(elem["team1"]) == 0:
    #             lobbyString += "empty"
    #         else:
    #             lobbyString += "\n"
    #         for player in elem["team1"]:
    #             lobbyString += player + "\n"
    #         lobbyString += "```\n**Defenders**\n```"
    #         if len(elem["team2"]) == 0:
    #             lobbyString += "empty"
    #         else:
    #             lobbyString += "\n"
    #         for player in elem["team2"]:
    #             lobbyString += player + "\n"
    #         lobbyString += "```"
    return lobbyString


def addPlayerToTeam1(discordName, guildID, gameID):
    if checkIfPlayerInGame(discordName, guildID, gameID) == True:
        return
    target = db["games"]
    query = {"guildID": guildID, "gameID": gameID}
    result = target.update_one(query, {"$push": {"players": discordName}})
    result2 = target.update_one(query, {"$push": {"team1": discordName}})

def addPlayerToTeam2(discordName, guildID, gameID):
    if checkIfPlayerInGame(discordName, guildID, gameID) == True:
        return
    target = db["games"]
    query = {"guildID": guildID, "gameID": gameID}
    result = target.update_one(query, {"$push": {"players": discordName}})
    result2 = target.update_one(query, {"$push": {"team2": discordName}})

def checkIfPlayerInGame(discordName, guildID, gameID):
    target = db["games"]
    query = {"guildID": guildID, "gameID": gameID}
    result = target.find_one(query, {"players": 1})
    if discordName in result["players"]:
        return True
    else: 
        return False


def removePlayerFromGame(discordName, guildID, gameID):
    target = db["games"]
    query = {"guildID": guildID, "gameID": gameID}
    result = target.update_one(query, {"$pull": {"players": discordName}})
    result2 = target.update_one(query, {"$pull": {"team1": discordName}})
    result3 = target.update_one(query, {"$pull": {"team2": discordName}})

def updatePlayerELO(discordName, guildID, ratingChange):
    target = db["players"]
    query = {"discordName": discordName}
    result = target.find_one(query)["guildInfo"]
    for elem in result:
        if elem["guildID"] == str(guildID):
            elem["ELO"] += ratingChange
    result2 = target.update_one(query, {"$set":{"guildInfo": result}})
    

def team1Wins(guildID, gameID):
    target = db["games"]
    query = {"guildID": guildID, "gameID": gameID}
    result = target.update_one(query, {"$set": {"result": "team1"}})
    team1Players = target.find_one(query)["team1"]
    for discordName in team1Players:
        updatePlayerELO(discordName, guildID, 10)
    team2Players = target.find_one(query)["team2"]
    for discordName in team2Players:
        updatePlayerELO(discordName, guildID, -10)

def team2Wins(guildID, gameID):
    target = db["games"]
    query = {"guildID": guildID, "gameID": gameID}
    result = target.update_one(query, {"$set": {"result": "team2"}})
    team1Players = target.find_one(query)["team1"]
    for discordName in team1Players:
        updatePlayerELO(discordName, guildID, -10)
    team2Players = target.find_one(query)["team2"]
    for discordName in team2Players:
        updatePlayerELO(discordName, guildID, 10)

def startGame(guildID, gameID):
    target = db["games"]
    query = {"guildID": guildID, "gameID": gameID}
    result = target.update_one(query, {"$set": {"result": "in progress"}})

def cancelGame(guildID, gameID):
    target = db["games"]
    query = {"guildID": guildID, "gameID": gameID}
    result = target.update_one(query, {"$set": {"result": "canceled"}})

def getGameStats(guildID, gameID):
    # retrieve game using valorant API and add to gamesData collection
    # use first player in lobby list by fetching their valorantName
    pass


# gets how many kills a given user has across all stored Valorant games    
def getKills(valorantName):
    target = db['gamesData']
    result = (target.aggregate([
            {
                "$unwind": "$kills"
            },
            { 
                "$group": {
                    "_id": "$kills.killer_display_name", "total": {"$sum":1}
                }
            }
    ]))
    for elem in result:
        if elem["_id"] == valorantName:
            return elem
        else:
            return None
### Test Commands ###
          
# addDocument(Player("Velocity", "Velocity#300", "Velocity#9534", str(166422822296485888)).__dict__, "players")
# print(checkUser("Velocity#9534"))
# print(countInstances("discordName", "Velocity#300", str(166422822296485888) + "players"))
# removeDocument("discordName", "Velocity#9534", "players")
# print(checkUser("Velocity#9534"))
# print(checkGuild("Velocity#9534", 166422822296485888))
# addPlayerWithExistingGuild("Velocity#9534", 123, "Velocity")
# setCurrentLobbyStatus(166422822296485888, False)
# print(getCurrentLobbyStatus(166422822296485888))
# incrementGameID(166422822296485888)
# createGame(166422822296485888, Game(1, 166422822296485888).__dict__)
# print(addPlayerToTeam2("Velocity#9534", 166422822296485888, 1))
# print(drawLobby(166422822296485888, 1))
# print(getLobbyHeadCount(166422822296485888, 1))
# print(checkIfPlayerInGame("Velocity#9534", 166422822296485888, 1))
# removePlayerFromGame("Velocity#9534", 166422822296485888, 1)
# team1Wins(166422822296485888, 1)
# updatePlayerELO("Velocity#9534", 166422822296485888, 10)