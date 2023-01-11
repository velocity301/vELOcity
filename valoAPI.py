import requests
import json
from jsonHandler import *

# response = requests.get("https://api.henrikdev.xyz/valorant/v3/matches/na/Velocity/300")

# check if player exists
def checkPlayer(valorantName):
    name = valorantName.split("#")[0]
    discriminator = valorantName.split("#")[1]
    return requests.get(f"https://api.henrikdev.xyz/valorant/v1/account/{name}/{discriminator}").json()["status"]


def getLastGame(valorantName):
    name = valorantName.split("#")[0]
    discriminator = valorantName.split("#")[1]
    return requests.get(f"https://api.henrikdev.xyz/valorant/v3/matches/na/{name}/{discriminator}").json()["data"][0]
    
def saveLastGame(valorantName):
    fileData = loadJson("gameStats.json")
    fileData.append(getLastGame(valorantName))
    saveJson(fileData, "gameStats.json")

def getTotalKills(valorantName):
    fileData = loadJson("gameStats.json")
    killcount = 0
    for game in fileData:
        for kill in game["kills"]:
            if kill["killer_display_name"] == valorantName:
                killcount += 1
    return killcount

def getKills(killer, target):
    fileData = loadJson("gamestats.json")
    killcount = 0
    for game in fileData:
        for kill in game["kills"]:
            if kill["killer_display_name"] == killer and kill["victim_display_name"] == target:
                killcount += 1
    return killcount         
