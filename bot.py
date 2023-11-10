from ast import alias
import json
import env
import random
import os
import datetime
import discord
from rasp import rasp
from discord.ext import commands, tasks
from discord.ext.commands import CommandNotFound

# Logging in and setting currently active servers
TOKEN = env.TOKEN
GUILD = env.GUILD

# Initialising bot basics
intents = discord.Intents().all()
bot = commands.Bot(command_prefix=["ZZZ ", "ZZz ", "Zzz ", "zzz ", "z.", "Z."], intents)


# First thing the bot does on launch
@bot.event
async def on_ready():
    print(f"{bot.user.name} reporting for duty!")


# Bot commands
## Quote command
@bot.command(aliases = ["q"])
async def quote(ctx, *, user_name: str = None):
    with open("quotes.json", "r") as quoteDB:
        data = json.load(quoteDB)
        if user_name:
            for person in data["users"]:
                if user_name in person["aliases"]:
                    quotes = person["quotes"]
                    if len(quotes)>0:
                        randQuote = random.choice(quotes)
                        await ctx.send(f'"{randQuote.capitalize()}" - {person["aliases"][0]}')
                    else:
                        await ctx.send(f"Sorry, {person['aliases'][0]} doesn't have any quotes.")
                    return
            await ctx.send(f"Sorry, {user_name} not found.")
        else:
            user = data["users"]
            if len(user)>0:
                person = random.choice(user)
                quotes = person["quotes"]
                if len(quotes)>0:
                    randQuote = random.choice(quotes)
                    await ctx.send(f'"{randQuote.capitalize()}" - {person["aliases"][0]}')
                else:
                    await ctx.send(f"Sorry, {person['aliases'][0]} doesn't have any quotes.")
            else:
                await ctx.send("Sorry, no user found.")

## Add Quote command
@bot.command(aliases = ["aq"])
async def add_quote(ctx, user_name: str, *, quote: str = None):
    if quote is None:
        await ctx.send("Please provide a quote.")
        return
    with open("quotes.json", "r") as quoteDB:
        data = json.load(quoteDB)
    for person in data["users"]:
        if user_name in person["aliases"]:
            id = person["aliases"][0]
            if quote in person["quotes"]:
                await ctx.send("That quote already exists.")
                return
            else:
                person["quotes"].append(quote)
                with open("quotes.json", "w") as quoteDB:
                    json.dump(data, quoteDB)
                await ctx.send(f"Quote \"{quote}\" has been added to {person['aliases'][0]}!")
                with open("lastQuote.json", "w") as lastQDB:
                    json.dump(quote, lastQDB)
                return
    await ctx.send(f"Sorry, {user_name} not found.")

## Last Quote command
@bot.command(aliases = ["lq", "last q"])
async def last_quote(ctx):
    with open("lastQuote.json", "r") as lastQDB:
        lastQuote = json.load(lastQDB)
    if lastQuote != "":
        await ctx.send(f"The last quote added was: \"{lastQuote}\"")
    else:
        await ctx.send("No quotes have been added yet.")

## List Quote command
@bot.command(aliases=["liq", "list q"])
async def list_quotes(ctx, *, user_name: str = None):
    with open("quotes.json", "r") as quoteDB:
        data = json.load(quoteDB)
    if user_name is None:
        await ctx.send("Please choose a person to list quotes from.")
    else:
        for person in data["users"]:
            if user_name in person["aliases"]:
                quotes = person["quotes"]
                if len(quotes)>0:
                    return_message = ""
                    for i in range(len(quotes)):
                        quote = "["+str(i + 1)+"] " + "\"" + quotes[i]+"\"" + "\n"
                        if len(return_message + quote) > 1800:
                            await ctx.send(str(return_message))
                            return_message = quote
                        else:
                            return_message += quote
                    await ctx.send(str(return_message))
                    return
        await ctx.send(f"Sorry, {user_name} not found.")

## Birthday command
@bot.command(aliases=["b", "bday"])
async def birthday(ctx, *, user_name: str = None):
    with open ("quotes.json", "r") as birthdayDB:
        data = json.load(quoteDB)
        if user_name is None:
            # Chooses nearest birthday
            today = datetime.now()
            nearest_date = None

            # Load JSON data
            data = json.load(json_data)
            for person in data["users"]:
                aliases = person.get("aliases", [])
                birthday_str = person.get("birthday", "")
                birthday = datetime.strptime(birthday_str, "%d/%m").replace(year=today.year)

                # Check if the birthday is in the future
                if birthday >= today:
                    days_until_birthday = (birthday - today).days

                    # Update nearest date if the current one is closer
                    if nearest_date is None or birthday < nearest_date:
                        nearest_date = birthday

                        await ctx.send(f"The next birthday is {user_name}'s on {nearest_date.strftime('%d/%m')}")
        else:
            for person in data["users"]:
                if user_name in person["aliases"]:
                    birthday = person["birthday"]
                    if birthday != "":
                        await ctx.send(f"{person['aliases'][0]}'s birthday is on {birthday}.")
                    else:
                        await ctx.send(f"Sorry, {person['aliases'][0]} doesn't have a birthday.")
                    return
            await ctx.send(f"Sorry, {user_name} not found.")
        
## Bot Update command
@bot.command(aliases=["upd"])
async def update_bot(ctx, *, user_name: str = None):
    	rasp.update_bot()

# Error handling    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send(f"Either the command wasn't used correctly.. || Or something is broken - (@andycap#5570) ||")
        return
    raise error
    
bot.run(TOKEN)