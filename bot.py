# import discord interactions
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

def objectToJson(object):
    return json.dumps(object.__dict__)

# TODO: add JSON to object functions for game and players

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
        self.username = "Name"
        self.ELO = 1000

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
    scope=ID,
)
async def button_test(ctx):
    await ctx.send("testing", components=button)

@bot.component("hello")
async def button_response(ctx):
    await ctx.send("You clicked the Button :O", ephemeral=True)

# 


# starts the bot
bot.start()
