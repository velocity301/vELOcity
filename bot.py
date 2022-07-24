import interactions
import json
import random
from valoAPI import *
from jsonHandler import *

# Open config file
configFile = loadJson("config.json")

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

#####################################################################################
# Test command to make sure bot is working 
# use "/test" in a discord channel to invoke
@bot.command(
    name="test",
    description="testing if bot is working",
    scope=ID
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
async def flame(ctx):
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
    if checkJson(ctx.author.name, "username", "players.json") == False:
        await ctx.popup(modal)
    else: 
        await ctx.send(f"You are already registered as {ctx.author.name}")

    @bot.modal("registerForm")
    async def modal_response(ctx, response: str):
        if checkPlayer(response) != 200:
            await ctx.send(f"Error finding {response} on Valorant servers.")
        else:
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
        await ctx.send(f"All records for {ctx.author.name} have been deleted.")
        

# Command to create a lobby for people to join
@bot.command(
    name="create", 
    description="Creates a lobby for players to join",
    scope=ID
)

async def create(ctx):
    @bot.component("team1")
    async def button_response1(ctx):
        if checkJson(ctx.author.name, "username", "players.json") == False:
            await ctx.send("You have to /register before you can join a game", ephemeral = True)
        else:
            addPlayerJson(ctx.author.name, "team1")
            if getLobbyHeadCount() == 10:
                await ctx.edit(embeds=[interactions.Embed(
                    title = f"Game {returnGameID()-1}", 
                    description = drawLobby())], 
                    components = gameControls2
                    )
            else:
                await ctx.edit(embeds=[interactions.Embed(
                    title = f"Game {returnGameID()-1}",
                    description = drawLobby())], 
                    components=gameControls)

    @bot.component("team2")
    async def button_response2(ctx):
        if checkJson(ctx.author.name, "username", "players.json") == False:
            await ctx.send("You have to /register before you can join a game", ephemeral = True)
        else:
            addPlayerJson(ctx.author.name, "team2")
            if getLobbyHeadCount() == 10:
                await ctx.edit(embeds=[interactions.Embed(
                    title = f"Game {returnGameID()-1}", 
                    description = drawLobby())], 
                    components = gameControls2
                    )
            else:
                await ctx.edit(embeds=[interactions.Embed(
                    title = f"Game {returnGameID()-1}",
                    description = drawLobby())], 
                    components=gameControls)

    @bot.component("leaveGame")
    async def button_response3(ctx):
        removePlayerJson(ctx.author.name)
        if getLobbyHeadCount() < 10:
            await ctx.edit(embeds=[interactions.Embed(
                title = f"Game {returnGameID()-1}",
                description = drawLobby())], 
                components=gameControls)
        elif getLobbyHeadCount() == 10:
            await ctx.edit(embeds=[interactions.Embed(
                title = f"Game {returnGameID()-1}", 
                description = drawLobby())], 
                components = gameControls2
                )
    
    @bot.component("startGame")
    async def button_response4(ctx):
        setGameResult("in progress")
        await ctx.edit(embeds=[interactions.Embed(
                title = f"Game {returnGameID()-1}", 
                description = drawLobby())], 
                components = gameControls3
                )

    @bot.component("team1Win")
    async def button_response5(ctx):
        setGameResult("team1")
        setWinELO("team1", returnGameID()-1)
        setLossELO("team2", returnGameID()-1)
        for elem in loadJson("games.json"):
            if elem["gameID"] == (returnGameID()-1):
                print(elem)
                username = elem["team1"][0]
                print(f"found: {username}")
        for elem in loadJson("players.json"):
            if elem["username"] == username:
                valorantName = elem["valorantName"]
        saveLastGame(valorantName)
        await ctx.edit(embeds=[interactions.Embed(
                title = f"Game {returnGameID()-1}", 
                description = drawLobby())], 
                components = []
                )

    @bot.component("team2Win")
    async def button_response5(ctx):
        setGameResult("team2")
        setWinELO("team2", returnGameID()-1)
        setLossELO("team1", returnGameID()-1)
        for elem in loadJson("games.json"):
            if elem["gameID"] == (returnGameID()-1):
                print(elem)
                username = elem["team1"][0]
                print(f"found: {username}")
        for elem in loadJson("players.json"):
            if elem["username"] == username:
                valorantName = elem["valorantName"]
        saveLastGame(valorantName)
        await ctx.edit(embeds=[interactions.Embed(
                title = f"Game {returnGameID()-1}", 
                description = drawLobby())], 
                components = []
                )

    @bot.component("cancelGame")
    async def button_response5(ctx):
        setGameResult("canceled")
        await ctx.edit(embeds=[interactions.Embed(
                title = f"Game {returnGameID()-1}", 
                description = drawLobby())], 
                components = []
                )

    newGame = Game(returnGameID())
    writeJson(newGame, "games.json")
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
        components=[joinTeam1, joinTeam2, leaveGame, cancelGame]
    )
    
    gameControls2 = interactions.ActionRow(
        components=[startGame, leaveGame, cancelGame]
    )

    gameControls3 = interactions.ActionRow(
        components=[team1Win, team2Win, cancelGame]
    )
    
    await ctx.send(embeds=[interactions.Embed(
                title = f"Game {returnGameID()-1}", 
                description = drawLobby())], 
                components = gameControls
                )

    print(f"Creating lobby")

# Command to display leaderboard sorted by ELO
# TODO: Have it only display 30 ppl per page and add buttons to switch pages
@bot.command(
    name="leaderboard",
    description="displays leaderboard of players sorted by ELO",
    scope=ID
)
async def leaderboard(ctx):
    print(getPlayersSorted())
    playerList = getPlayersSorted()
    column1 = ""
    column2 = ""
    for player in playerList:
        column1 += player[1] + "\n" # + ": " +str(player[0]) + "\n"
    for player in playerList:
        column2 += str(player[0]) + "\n"
    leaderboardEmbed = interactions.Embed(title="Leaderboard")
    leaderboardEmbed.add_field(name = "Player", value = column1, inline = True)
    leaderboardEmbed.add_field(name = "ELO", value = column2, inline = True)
    await ctx.send(embeds=[leaderboardEmbed])

@bot.command(
    name = "killedby",
    description="test how many times a player has killed another",
    scope=ID,
    options = [
        interactions.Option(
            name="killer",
            description="killer",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="target",
            description="target of kills",
            type=interactions.OptionType.STRING,
            required=True
        )
    ]
)

# Generate player cards


# shows number of times killer has killed target in all games
async def killedby(ctx, killer, target):
    killcount = getKills(killer, target)
    embed = interactions.Embed(title = f"{target} has been killed by {killer} {killcount} times.")
    await ctx.send(embeds=[embed])


@bot.command(
    name="embedtest", 
    description="testing embed function",
    scope=ID
)

async def embedtest(ctx):
    print("test before embed creation")
    embed=interactions.Embed(title = "Test", description = "test description")
    await ctx.send(embeds=[embed])

# starts the bot
bot.start()
