# import interactions
# import json
# import random
# from valoAPI import *
# from jsonHandler import *
# from mongoDBHandler import *

# # Open config file
# configFile = loadJson("config.json")

# TOKEN = configFile['TOKEN']
# ID = int(configFile['ID'])
# print(TOKEN+" "+str(ID))

# bot = interactions.Client(token=TOKEN)




# @bot.component("team1")
# async def button_response1(ctx):
#     discordName = str(ctx.user) + "#" + str(ctx.user.discriminator)
#     if countInstancesMongo("discordName", discordName, str(guild) + "players") == 0:
#         await ctx.send("You have to /register before you can join a game", ephemeral = True)
#     else:
#         addPlayerJson(ctx.author.name, "team1")
#         if getLobbyHeadCount() == 10:
#             await ctx.edit(embeds=[interactions.Embed(
#                 title = f"Game {returnGameID()-1}", 
#                 description = drawLobby())], 
#                 components = gameControls2
#                 )
#         else:
#             await ctx.edit(embeds=[interactions.Embed(
#                 title = f"Game {returnGameID()-1}",
#                 description = drawLobby())], 
#                 components=gameControls)

# @bot.component("team2")
# async def button_response2(ctx, gameControls, gameControls2):
#     if checkJson(ctx.author.name, "username", "players.json") == False:
#         await ctx.send("You have to /register before you can join a game", ephemeral = True)
#     else:
#         addPlayerJson(ctx.author.name, "team2")
#         if getLobbyHeadCount() == 10:
#             await ctx.edit(embeds=[interactions.Embed(
#                 title = f"Game {returnGameID()-1}", 
#                 description = drawLobby())], 
#                 components = gameControls2
#                 )
#         else:
#             await ctx.edit(embeds=[interactions.Embed(
#                 title = f"Game {returnGameID()-1}",
#                 description = drawLobby())], 
#                 components=gameControls)

# @bot.component("leaveGame")
# async def button_response3(ctx):
#     removePlayerJson(ctx.author.name)
#     if getLobbyHeadCount() < 10:
#         await ctx.edit(embeds=[interactions.Embed(
#             title = f"Game {returnGameID()-1}",
#             description = drawLobby())], 
#             components=gameControls)
#     elif getLobbyHeadCount() == 10:
#         await ctx.edit(embeds=[interactions.Embed(
#             title = f"Game {returnGameID()-1}", 
#             description = drawLobby())], 
#             components = gameControls2
#             )

# @bot.component("startGame")
# async def button_response4(ctx):
#     setGameResult("in progress")
#     await ctx.edit(embeds=[interactions.Embed(
#             title = f"Game {returnGameID()-1}", 
#             description = drawLobby())], 
#             components = gameControls3
#             )

# @bot.component("team1Win")
# async def button_response5(ctx):
#     setGameResult("team1")
#     setWinELO("team1", returnGameID()-1)
#     setLossELO("team2", returnGameID()-1)
#     for elem in loadJson("games.json"):
#         if elem["gameID"] == (returnGameID()-1):
#             print(elem)
#             username = elem["team1"][0]
#             print(f"found: {username}")
#     for elem in loadJson("players.json"):
#         if elem["username"] == username:
#             valorantName = elem["valorantName"]
#     saveLastGame(valorantName)
#     await ctx.edit(embeds=[interactions.Embed(
#             title = f"Game {returnGameID()-1}", 
#             description = drawLobby())], 
#             components = []
#             )

# @bot.component("team2Win")
# async def button_response5(ctx):
#     setGameResult("team2")
#     setWinELO("team2", returnGameID()-1)
#     setLossELO("team1", returnGameID()-1)
#     for elem in loadJson("games.json"):
#         if elem["gameID"] == (returnGameID()-1):
#             print(elem)
#             username = elem["team1"][0]
#             print(f"found: {username}")
#     for elem in loadJson("players.json"):
#         if elem["username"] == username:
#             valorantName = elem["valorantName"]
#     saveLastGame(valorantName)
#     await ctx.edit(embeds=[interactions.Embed(
#             title = f"Game {returnGameID()-1}", 
#             description = drawLobby())], 
#             components = []
#             )

# @bot.component("cancelGame")
# async def button_response5(ctx):
#     setGameResult("canceled")
#     await ctx.edit(embeds=[interactions.Embed(
#             title = f"Game {returnGameID()-1}", 
#             description = drawLobby())], 
#             components = []
#             )
