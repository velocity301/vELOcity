import interactions
import json
import random
from valoAPI import *
from jsonHandler import *
import mongoDBHandler as Mongo

# Open config file
configFile = loadJson("config.json")

TOKEN = configFile['TOKEN']
# intents = interactions.Intents(guilds = True)
# intents.guilds = True

bot = interactions.Client(token=TOKEN, intents=interactions.Intents.ALL)


# classes for storing data
class Game:
    def __init__(self, gameID, guildID): 
        self.players = []
        self.team1 = []
        self.team2 = []
        self.map = random.choice(["Split", "Ascent", "Icebox", "Breeze", "Bind", "Haven", "Fracture", "Pearl"])
        self.gameID = gameID
        self.result = "waiting to start"
        self.guildID = guildID

class Player:
    def __init__(self, username, valorantName, discordName, guildID):
        self.discordName = discordName
        self.valorantName = valorantName
        self.guildInfo = [{"guildID": str(guildID), "ELO": 1000, "username": username}]

# class for allowing buttons to be instanced
# class LobbyButton:
#     def __init__(self, _style, _label, _custom_id, guildID, gameID):
#         self.guildID = guildID
#         self.gameID = gameID
#         self.buttonObject = interactions.Button(style=_style, label=_label, custom_id=_custom_id)
        
#         # add button functions here
#         @bot.component("test")
#         async def button_callback(ctx):
#             gameControls = interactions.ActionRow(
#                 components=[self.buttonObject])
#             await ctx.edit(embeds=[interactions.Embed(
#                 title = f"Game {self.guildID}, {self.gameID}", 
#                 description = "asdf")], 
#                 components = gameControls
#                 )


#####################################################################################
### Commands ###

# execute this when the bot is added to a guild
# adds a document to the config collection 
# with the guild ID and initializes the gameID to 1
# TODO: try to make this work with on_guild_join instead of being a command
@bot.command(
    name="setup", 
    description="run this command to create the configuration files for your server"
)
async def setup(ctx):
    guildID = int(ctx.guild_id)
    print(f'Setting up Guild: {guildID}')
    if Mongo.countInstances("guildID", guildID, "config") > 0:
        await ctx.send("This guild is already set up.")
    elif Mongo.countInstances("guildID", guildID, "config") == 0:
        Mongo.addDocument({"guildID": guildID, "gameID": 1, "currentLobby": False}, "config")
        await ctx.send("Your guild has been initialized.")

@bot.command(
    name="reset", 
    description="run this command to remove the configuration files for your server"
)
async def reset(ctx):
    guildID = int(ctx.guild_id)
    print(f'Resetting guild info for Guild: {guildID}')
    if Mongo.countInstances("guildID", guildID, "config") == 0:
        await ctx.send("This guild has no data to reset.")
    elif Mongo.countInstances("guildID", guildID, "config") > 0:
        Mongo.removeDocument("guildID", guildID, "config")
        await ctx.send("Your guild has been reset.")


# Test command to make sure bot is working 
# use "/test" in a discord channel to invoke
@bot.command(
    name="test",
    description="testing if bot is working",
    # scope=ID
)
async def test(ctx: interactions.CommandContext):
    await ctx.send("Hi there!")

# repeats a message
@bot.command(
    name="echo",
    description="repeats a message",
    # scope=ID,
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
    # scope=ID
)
async def flame(ctx):
    await ctx.send(f"{ctx.target.user.username} sucks.")


# Command to register a user in the database

@bot.command(
    name="register",
    description="Registers a player in the database",
    # scope=ID
)
async def register(ctx):
    guildID = ctx.guild_id
    discordName = str(ctx.user) + "#" + str(ctx.user.discriminator)
    print(f"Registering user {discordName} in server {guildID}")
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
    
    if Mongo.checkGuild(discordName, guildID) == False:
        await ctx.popup(modal)
    else: 
        await ctx.send(f"You are already registered as {discordName}")
@bot.modal("registerForm")
async def modal_response(ctx, response: str):
    guildID = ctx.guild_id
    discordName = str(ctx.user) + "#" + str(ctx.user.discriminator)
    if checkPlayer(response) != 200:
        await ctx.send(f"Error finding {response} on Valorant servers.")
    else:
        if Mongo.checkUser(discordName) == True and Mongo.checkGuild(discordName, guildID) == False:
            Mongo.addPlayerWithExistingGuild(discordName, guildID, ctx.author.name)
            await ctx.send(f"You have now been registered as: {discordName}. You are also registered in other guild(s)")
        else:
            print("adding player")
            Mongo.addDocument(Player(ctx.author.name, response, discordName, guildID).__dict__, "players")
            print("player added")
            await ctx.send(f"You have been registered as: {discordName}")

# Deletes the user invoking the command from the database
@bot.command(
    name="deleteme",
    description="Deletes a player in the database",
    # scope=ID
)
async def deleteme(ctx):
    guildID = ctx.guild_id
    discordName = str(ctx.user) + "#" + str(ctx.user.discriminator)
    print(f"Deleting user {ctx.author.name}")
    if Mongo.checkUser(discordName) == 0:
        await ctx.send(f"You are not registered")
    else:
        Mongo.removeDocument("discordName", discordName, "players")
        await ctx.send(f"All records for {discordName} have been deleted.")

  
# Lobby controls for create command 
def gameControls(gameStatus):
    joinTeam1 = interactions.Button(
        style=interactions.ButtonStyle.PRIMARY, 
        label="Join Attackers",
        custom_id="joinAttackers" 
    )
    joinTeam2 = interactions.Button(
        style=interactions.ButtonStyle.PRIMARY, 
        label="joinDefenders",
        custom_id="joinDefenders"  
    )
    leaveGame = interactions.Button(
        style=interactions.ButtonStyle.SECONDARY, 
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
        custom_id="attackersWin"
    )

    team2Win = interactions.Button(
        style=interactions.ButtonStyle.PRIMARY,
        label="Team 2 Wins", 
        custom_id="defendersWin"
    )

    cancelGame = interactions.Button(
        style=interactions.ButtonStyle.DANGER,
        label="Cancel Game", 
        custom_id="cancelGame"
)
    if gameStatus == "space":
        return [joinTeam1, joinTeam2, leaveGame, cancelGame]
    elif gameStatus == "full":
        return [startGame, leaveGame, cancelGame]
    elif gameStatus == "in progress":
        return [team1Win, team2Win, cancelGame]
    elif gameStatus == "completed":
        return []
        
# Command to create a lobby for people to join
@bot.command(
    name="create", 
    description="Creates a lobby for players to join",
    # scope=ID
)
async def create(ctx):
    guildID = int(ctx.guild_id)
    if Mongo.getCurrentLobbyStatus(guildID) == True:
        await ctx.send("A lobby already exists")
    elif Mongo.getCurrentLobbyStatus(guildID) == False:
        print(Mongo.getCurrentLobbyStatus(guildID))
        Mongo.createGame(Game(Mongo.getCurrentGameID(guildID), guildID).__dict__)
        Mongo.setCurrentLobbyStatus(guildID, True)
        await ctx.send(embeds=[interactions.Embed(
                title = f"Game {Mongo.getCurrentGameID(guildID)}", 
                description = Mongo.drawLobby(guildID, Mongo.getCurrentGameID(guildID)))], 
                components = gameControls("space")
                )



@bot.component("joinAttackers")
async def joinAttackers(ctx):
    guildID = int(ctx.guild_id)
    discordName = str(ctx.user) + "#" + str(ctx.user.discriminator)
    if Mongo.checkGuild(discordName, guildID) == False:
        await ctx.send("You have to /register before you can join a game", ephemeral = True)
    else:
        Mongo.addPlayerToTeam1(discordName, guildID, Mongo.getCurrentGameID(guildID))
        if Mongo.getLobbyHeadCount(guildID, Mongo.getCurrentGameID(guildID)) == 10: 
            await ctx.edit(embeds=[interactions.Embed(
                title = f"Game {Mongo.getCurrentGameID(guildID)}", 
                description = Mongo.drawLobby(guildID, Mongo.getCurrentGameID(guildID)))], 
                components = gameControls("full")
                )
        else:
            await ctx.edit(embeds=[interactions.Embed(
                title = f"Game {Mongo.getCurrentGameID(guildID)}",
                description = Mongo.drawLobby(guildID, Mongo.getCurrentGameID(guildID)))], 
                components = gameControls("space")
            )

@bot.component("joinDefenders")
async def joinDefenders(ctx):
    guildID = int(ctx.guild_id)
    discordName = str(ctx.user) + "#" + str(ctx.user.discriminator)
    if Mongo.checkGuild(discordName, guildID) == False:
        await ctx.send("You have to /register before you can join a game", ephemeral = True)
    else:
        Mongo.addPlayerToTeam2(discordName, guildID, Mongo.getCurrentGameID(guildID))
        if Mongo.getLobbyHeadCount(guildID, Mongo.getCurrentGameID(guildID)) == 10: 
            await ctx.edit(embeds=[interactions.Embed(
                title = f"Game {Mongo.getCurrentGameID(guildID)}", 
                description = Mongo.drawLobby(guildID, Mongo.getCurrentGameID(guildID)))], 
                components = gameControls("full")
                )
        else:
            await ctx.edit(embeds=[interactions.Embed(
                title = f"Game {Mongo.getCurrentGameID(guildID)}",
                description = Mongo.drawLobby(guildID, Mongo.getCurrentGameID(guildID)))], 
                components = gameControls("space")
            )
@bot.component("leaveGame")
async def leaveGame(ctx):
    guildID = int(ctx.guild_id)
    discordName = str(ctx.user) + "#" + str(ctx.user.discriminator) 
    Mongo.removePlayerFromGame(discordName, guildID, Mongo.getCurrentGameID(guildID))
    if Mongo.getLobbyHeadCount(guildID, Mongo.getCurrentGameID(guildID)) < 10:
        await ctx.edit(embeds=[interactions.Embed(
            title = f"Game {Mongo.getCurrentGameID(guildID)}",
            description = Mongo.drawLobby(guildID, Mongo.getCurrentGameID(guildID)))], 
            components = gameControls("space")
        )
    elif getLobbyHeadCount() == 10:
        await ctx.edit(embeds=[interactions.Embed(
            title = f"Game {Mongo.getCurrentGameID(guildID)-1}", 
            description = Mongo.drawLobby(guildID, Mongo.getCurrentGameID(guildID)))], 
            components = gameControls("full")
            )

@bot.component("startGame")
async def startGame(ctx):
    guildID = int(ctx.guild_id)
    Mongo.setCurrentLobbyStatus("in progress")
    await ctx.edit(embeds=[interactions.Embed(
            title = f"Game {Mongo.getCurrentGameID(guildID)}", 
            description = Mongo.drawLobby(guildID, Mongo.getCurrentGameID(guildID)))], 
            components = gameControls("in progress")
            )

@bot.component("team1Win")
async def team1Win(ctx):
    guildID = int(ctx.guild_id)
    Mongo.team1Wins(guildID, Mongo.getCurrentGameID)
    Mongo.setCurrentLobbyStatus(guildID, "team1")
    Mongo.incrementGameID(guildID)
    # saveLastGame(valorantName) write function to grab first player's valorant name in lobby
    await ctx.edit(embeds=[interactions.Embed(
            title = f"Game {Mongo.getCurrentGameID(guildID)-1}", 
            description = Mongo.drawLobby(guildID, Mongo.getCurrentGameID(guildID)-1))], 
            components = []
            )

@bot.component("team2Win")
async def team2Win(ctx):
    guildID = int(ctx.guild_id)
    Mongo.team2Wins(guildID, Mongo.getCurrentGameID)
    Mongo.setCurrentLobbyStatus(guildID, "team2")
    Mongo.incrementGameID(guildID)
    # saveLastGame(valorantName) write function to grab first player's valorant name in lobby
    await ctx.edit(embeds=[interactions.Embed(
            title = f"Game {Mongo.getCurrentGameID(guildID)-1}", 
            description = Mongo.drawLobby(guildID, Mongo.getCurrentGameID(guildID)-1))], 
            components = []
            )

@bot.component("cancelGame")
async def cancelGame(ctx):
    guildID = int(ctx.guild_id)
    Mongo.setCurrentLobbyStatus(guildID, False)
    Mongo.incrementGameID(guildID)
    await ctx.edit(embeds=[interactions.Embed(
            title = f"Game {Mongo.getCurrentGameID(guildID)-1}", 
            description = Mongo.drawLobby(guildID, Mongo.getCurrentGameID(guildID)-1))], 
            components = []
            )
# TODO: write cancel command
# @bot.command(
#     name="cancel"
#     description="cancels the currently active game in the server"
# )




# Command to display leaderboard sorted by ELO
# TODO: Have it only display 30 ppl per page and add buttons to switch pages
@bot.command(
    name="leaderboard",
    description="displays leaderboard of players sorted by ELO",
    # scope=ID
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
    # scope=ID,
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
    # scope=ID
)

async def embedtest(ctx):
    print("test before embed creation")
    embed=interactions.Embed(title = "Test", description = "test description")
    await ctx.send(embeds=[embed])

# starts the bot
bot.start()
