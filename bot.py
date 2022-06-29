import discord
import interactions
import json
import random

# Open config file
with open("config.json") as f:
    configFile = json.load(f)
TOKEN = configFile['TOKEN']
ID = int(configFile['ID'])
print(TOKEN+" "+str(ID))

bot = interactions.Client(token=TOKEN)
#####################################################################################
# JSON Handling functions

def objectToJson(object1):
    return json.dumps(object1.__dict__)

def writeJson(newData, fileName):
    with open(fileName,'r+') as f:
        fileData = json.load(f)
        fileData.append(newData.__dict__)
        f.seek(0)
        json.dump(fileData, f)

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
            print(elem)
            elem[newAttribute] = newAttributeDefault
        f.seek(0)
        json.dump(fileData, f)

def incrementGameID():
    with open("config.json", 'r+') as f:
        fileData = json.load(f)
        print(fileData)
        fileData["gameID"]+=1
        print(fileData)
        f.seek(0)
        json.dump(fileData, f)

def returnGameID():
    with open("config.json", 'r+') as f:
        fileData = json.load(f)
        print(fileData)
        return fileData["gameID"] 

#####################################################################################
# classes for storing data
class Game:
    def __init__(self, gameID): 
        with open("config.json") as f:
            configFile = json.load(f)
            self.gameID = configFile['gameID']
        self.players = []
        self.team1 = ["-----","-----","-----","-----","-----"]
        self.team2 = ["-----","-----","-----","-----","-----"]
        self.map = random.choice(["Split", "Ascent", "Icebox", "Breeze", "Bind", "Haven", "Fracture", "Pearl"])
        self.gameID = gameID
class Player:
    def __init__(self, username, ELO):
        self.username = username
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

# Registers the user who types the command into the player database

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

# button test can use to join game or something
button = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label="hello world!",
    custom_id="hello"
)

@bot.command(
    name="button_test",
    description="This is the first command I made!",
    scope=ID
)
async def button_test(ctx):
    await ctx.send("testing", components=button)

@bot.component("hello")
async def button_response(ctx):
    await ctx.send("You clicked the Button :O")

# Command to register a user in the database
@bot.command(
    name="register",
    description="Registers a player in the database",
    scope=ID
)

async def register(ctx):
    print(f"Registering user {ctx.author.name}")
    if (checkJson(ctx.author.name, "username", "players.json")==False):
        writeJson(Player(ctx.author.name, 1000), "players.json")
        await ctx.send(f"You have been registered as {ctx.author.name}")
    else:
        await ctx.send(f"You are already registered as {ctx.author.name}")

# Command to create a lobby for people to join
@bot.command(
    name="create", 
    description="Creates a lobby for players to join",
    scope=ID
)

async def create(ctx):
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
    gameControls = interactions.ActionRow(
        components=[joinTeam1, joinTeam2]
    )
    gameDetailsString = f"Map: {newGame.map}\n\n**Attackers**\n```"
    
    # ```\n-----\n-----\n-----\n-----\n-----\n```
    # **Defenders**\n```\n-----\n-----\n-----\n-----\n----- ```"
    
    
    await ctx.send(gameDetailsString, components=gameControls)

    print(f"Creating lobby")
    # writeJson(Game(), "games.json")

    #add player who invoked command to the game's team 1
    #create a message that has the game's two teams and map name with two buttons that say join team

@bot.component("team1")
async def button_response1(ctx, gameDetailsString):
    await ctx.edit(f"{ctx.author.name} joined team 1")

@bot.component("team2")
async def button_response2(ctx):
    await ctx.edit(f"{ctx.author.name} joined team 2")

@bot.component("leaveGame")
async def button_response2(ctx):
    await ctx.edit(f"{ctx.author.name} left the game")

# starts the bot
bot.start()
