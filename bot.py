import interactions
from tokenId import *

bot = interactions.Client(token=TOKEN)


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
    description="registers a user",
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
