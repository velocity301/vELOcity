import requests
import json
from jsonHandler import *
# Stats ideas
# how far on avg is a player from bomb plants
# how far on avg is a player from kills
# avg damage done to allies
# number of kills on specific player
# number of deaths to specific player
# headshot percentage
# friendly fire

# response = requests.get("https://api.henrikdev.xyz/valorant/v3/matches/na/Velocity/300")

# print("test")
# print(response.json())
# saveJson(response.json()["data"][0], "test.json")
fileData = loadJson("gameStats.json")
killcount = 0
games = fileData
for game in games:
    for kill in game["kills"]:
        # print(kill["killer_display_name"])
        if kill["killer_display_name"] == "Velocity#300":
            killcount += 1
            print(killcount)
    # for kill in games["kills"]:
    #     # print(kill["killer_display_name"])
    #     print(kill["kill_time_in_round"])
    #     # if kill["killer_display_name"] == "Velocity#300":
    #         # killcount += 1
