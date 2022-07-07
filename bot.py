import discord
import interactions
import json
import random
import riotAPI
from jsonHandler import *

# Open config file
with open("config.json") as f:
    configFile = json.load(f)
TOKEN = configFile['TOKEN']
ID = int(configFile['ID'])
print(TOKEN+" "+str(ID))

bot = interactions.Client(token=TOKEN)

# classes for storing data
class Game:
    def __init__(self, gameID): 
        with open("config.json") as f:
            configFile = json.load(f)
            self.gameID = configFile['gameID']
        self.players = []
        self.team1 = []
        self.team2 = []
        self.map = random.choice(["Split", "Ascent", "Icebox", "Breeze", "Bind", "Haven", "Fracture", "Pearl"])
        self.gameID = gameID
        self.result = "waiting to start"
class Player:
    def __init__(self, username, valorantName, discordName):
        self.username = username
        self.valorantName = valorantName
        self.discordName = discordName
        self.ELO = 1000
        self.wins = 0
        self.losses = 0
        self.kills = 0
        self.deaths = 0
        self.assists = 0

#####################################################################################
# Test command to make sure bot is working 
# use "/test" in a discord channel to invoke
@bot.command(
    name="test",
    description="testing if bot is working",
    scope=ID,
)
async def test(ctx: interactions.CommandContext):
    await ctx.send("Hi there!")

# repeats a message
@bot.command(
    name="echo",
    description="repeats a message",
    scope=ID,
    options = [
        interactions.Option(
            name="text",
            description="What you want to say",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def echo(ctx: interactions.CommandContext, text: str):
    await ctx.send(f"{text}")

# Menu based command 
# can right click usernames and do things to them
@bot.command(
    type=interactions.ApplicationCommandType.USER,
    name="flame",
    scope=ID
)
async def test(ctx):
    await ctx.send(f"{ctx.target.user.username} sucks.")


# Command to register a user in the database
@bot.command(
    name="register",
    description="Registers a player in the database",
    scope=ID
)
async def register(ctx):
    print(f"Registering user {ctx.author.name}")
    registerText = interactions.TextInput(
        style=interactions.TextStyleType.SHORT,
        label="What is your Valorant ID? (e.g. Velocity#300)",
        custom_id="registerForm",
        min_length=1,
        max_length=25
    )
    modal = interactions.Modal(
        title="Registration Form",
        custom_id="registerForm",
        components=[registerText]
    )
    await ctx.popup(modal)

    @bot.modal("registerForm")
    async def modal_response(ctx, response: str):
        if (checkJson(ctx.author.name, "username", "players.json")==False):
            discordName = str(ctx.user) + "#" + str(ctx.user.discriminator)
            print(discordName)
            writeJson(Player(ctx.author.name, response, discordName), "players.json")
            await ctx.send(f"You have been registered as: {ctx.author.name}")
        else:
            await ctx.send(f"You are already registered as {ctx.author.name}")

# Deletes the user invoking the command from the database
@bot.command(
    name="deleteme",
    description="Deletes a player in the database",
    scope=ID
)

async def deleteme(ctx):
    print(f"Deleting user {ctx.author.name}")
    discordName = str(ctx.user) + "#" + str(ctx.user.discriminator)
    if checkJson(discordName, "discordName", "players.json") == False:
        await ctx.send(f"You are not registered")
    else:
        deletePlayer(discordName)
        

# Command to create a lobby for people to join
@bot.command(
    name="create", 
    description="Creates a lobby for players to join",
    scope=ID
)

async def create(ctx):
    
    @bot.component("team1")
    async def button_response1(ctx):
        addPlayerJson(ctx.author.name, "team1")
        if getLobbyHeadCount() == 10:
            await ctx.edit(drawLobby(), components = gameControls2)
        else:
            await ctx.edit(drawLobby(), components=gameControls)

    @bot.component("team2")
    async def button_response2(ctx):
        addPlayerJson(ctx.author.name, "team2")
        if getLobbyHeadCount() == 10:
            await ctx.edit(drawLobby(), components = gameControls2)
        else:
            await ctx.edit(drawLobby(), components=gameControls)

    @bot.component("leaveGame")
    async def button_response3(ctx):
        removePlayerJson(ctx.author.name)
        if getLobbyHeadCount() < 10:
            await ctx.edit(drawLobby(), components = gameControls)
        elif getLobbyHeadCount() == 10:
            await ctx.edit(drawLobby(), components=gameControls2)
    
    @bot.component("startGame")
    async def button_response4(ctx):
        setGameResult("in progress")
        gameControls=interactions.ActionRow(
            components=[team1Win, team2Win, cancelGame]
        )
        await ctx.edit(drawLobby(), components=gameControls)

    @bot.component("team1Win")
    async def button_response5(ctx):
        setGameResult("team1")
        setWinELO("team1", returnGameID()-1)
        setLossELO("team2", returnGameID()-1)
        await ctx.edit(drawLobby(), components=[])

    @bot.component("team2Win")
    async def button_response5(ctx):
        setGameResult("team2")
        setWinELO("team2", returnGameID()-1)
        setLossELO("team1", returnGameID()-1)
        await ctx.edit(drawLobby(), components=[])

    @bot.component("cancelGame")
    async def button_response5(ctx):
        setGameResult("canceled")
        await ctx.edit(drawLobby(), components=[])

    gameID = returnGameID()
    newGame = Game(gameID)
    writeJson(newGame, "games.json")
    print(newGame.gameID)
    incrementGameID()

    joinTeam1 = interactions.Button(
        style=interactions.ButtonStyle.PRIMARY, 
        label="Join Attackers",
        custom_id="team1"    
    )
    joinTeam2 = interactions.Button(
        style=interactions.ButtonStyle.PRIMARY, 
        label="Join Defenders",
        custom_id="team2"   
    )
    leaveGame = interactions.Button(
        style=interactions.ButtonStyle.PRIMARY, 
        label="Exit lobby",
        custom_id="leaveGame"   
    )
    startGame = interactions.Button(
        style=interactions.ButtonStyle.PRIMARY,
        label="Start Game", 
        custom_id="startGame"
    )

    team1Win = interactions.Button(
        style=interactions.ButtonStyle.PRIMARY,
        label="Team 1 Wins", 
        custom_id="team1Win"
    )

    team2Win = interactions.Button(
        style=interactions.ButtonStyle.PRIMARY,
        label="Team 2 Wins", 
        custom_id="team2Win"
    )

    cancelGame = interactions.Button(
        style=interactions.ButtonStyle.PRIMARY,
        label="Cancel Game", 
        custom_id="cancelGame"
    )

    gameControls = interactions.ActionRow(
        components=[joinTeam1, joinTeam2, leaveGame]
    )
    
    gameControls2 = interactions.ActionRow(
        components=[startGame, leaveGame]
    )

    gameControls3 = interactions.ActionRow(
        components=[team1Win, team2Win, cancelGame]
    )
    
    await ctx.send(drawLobby(), components=gameControls)

    print(f"Creating lobby")

# Command to display leaderboard sorted by ELO
@bot.command(
    name="leaderboard",
    description="displays leaderboard of players sorted by ELO",
    scope=ID
)
async def leaderboard(ctx):
    print(getPlayersSorted())
    playerList = getPlayersSorted()
    leaderboard = "```"
    for player in playerList:
        leaderboard += player[1] + ": " +str(player[0]) + "\n"
    leaderboard += "```"
    await ctx.send(leaderboard)

# @bot.command()
# async def embed(ctx):
#     embed=discord.Embed(title="Sample Embed", url="https://realdrewdata.medium.com/", description="This is an embed that will show how to build an embed and the different components", color=0xFF5733)
#     await ctx.send(embed=embed)    

# starts the bot
bot.start()
