import discord
import interactions
import json

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
            

#####################################################################################
# classes for storing data
class Game:
    def __init__(self, players, team1, team2, map): 
        self.players = players
        self.team1 = team1
        self.team2 = team1
        self.map = map

class Player:
    def __init__(self, username, ELO):
        self.username = username
        self.ELO = ELO



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
async def register(ctx: interactions.CommandContext, text: str):
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
    await ctx.send("You clicked the Button :O", ephemeral=True)

# Command to register a user in the database
@bot.command(
    name="register",
    description="Registers a player in the database",
    scope=ID
)

async def register(ctx):
    print(f"Registering user {ctx.author.name}")
    if (checkJson(ctx.author.name, "username", "players.json")==False):
        player = Player(ctx.author.name, 1000)
        writeJson(player, "players.json")
        await ctx.send(f"You have been registered as {ctx.author.name}")
    else:
        await ctx.send(f"You are already registered as {ctx.author.name}")




# starts the bot
bot.start()
