from ast import alias
import json
import env
import random
import os
import discord
from discord.ext import commands, tasks
from discord.ext.commands import CommandNotFound

# Logging in and setting currently active servers
TOKEN = env.TOKEN
GUILD = env.GUILD

# Initialising bot basics
intents = discord.Intents().all()
bot = commands.Bot(command_prefix=["ZZZ ", "ZZz ", "Zzz ", "zzz ", "z.", "Z."], intents = discord.Intents().all())


# First thing the bot does on launch
@bot.event
async def on_ready():
    print(f"{bot.user.name} reporting for duty!")

# Bot looping

# Bot commands
@bot.command(aliases = ["q"])
async def quote(ctx, arg = ""):
    with open("quoteList.json") as quoteDB:
        quoteList = json.load(quoteDB)
    if arg == "":
        user = random.choice(list(quoteList))
        randomNum = random.randint(0, len(quoteList[user]) - 1)
        await ctx.send("\""+str(quoteList[user][randomNum]).capitalize()+"\" - " + str(user).capitalize())
    elif arg != "":
        if arg not in quoteList:
            await ctx.send("That person isn't in the list.")
            return
        desired_quote = random.choice(list(quoteList[arg]))
        await ctx.send("\""+str(desired_quote).capitalize() + "\"")

# Error handling    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send(f"That command doesn't exist.. yet? Ask and ye shall (maybe) receive! \n ||(Or use help)||")
        return
    raise error

bot.run(TOKEN)