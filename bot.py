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
bot = commands.Bot(command_prefix = ["Z.", "z.", "Zzz ", "zzz"], intents = discord.Intents().all())

# First thing the bot does on launch
@bot.event
async def on_ready():
    print(f"{bot.user.name} reporting for duty!")

# Bot looping

# Bot commands



# Error handling


bot.run(TOKEN)