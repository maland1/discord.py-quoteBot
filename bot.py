from ast import alias
import json
import random
import os
from datetime import datetime
import discord
from rasp import rasp
from discord.ext import commands, tasks
from discord.ext.commands import CommandNotFound

# Logging in and setting currently active servers
with open("env.json", "r") as env:    
    data = json.load(env)
    TOKEN = data.get("secret_key")
    GUILDS = data.get("guilds")


# Initialising bot basics
bot = commands.Bot(command_prefix=["zzz "], intents = discord.Intents().all())


# First thing the bot does on launch
@bot.event
async def on_ready():
    print(f"{bot.user.name} reporting for duty!")


# Bot commands
## Quote command
@bot.command(aliases = ["q"])
async def quote(ctx, *, userID: str = None):
    with open("quotes.json", "r") as quoteDB:
        data = json.load(quoteDB)

        if userID:
            for name in data["users"]:
                if userID in name["aliases"]:
                    quotes = name["quotes"]

                    if len(quotes)>0:
                        randomQuote = random.choice(quotes)
                        await ctx.send(f'"{randomQuote}" - {name["aliases"][0]}')

                    else:
                        await ctx.send(f"Sorry, {name['aliases'][0]} doesn't have any quotes.")

                    return
            await ctx.send(f"Sorry, {userID} not found.")
        else:
            user = data["users"]

            if len(user)>0:
                name = random.choice(user)
                quotes = name["quotes"]

                if len(quotes)>0:
                    randomQuote = random.choice(quotes)
                    await ctx.send(f'"{randomQuote}" - {name["aliases"][0]}')

                else:
                    await ctx.send(f"Sorry, {name['aliases'][0]} doesn't have any quotes.")

            else:
                await ctx.send("Sorry, no user found.")

## Add Quote command
@bot.command(aliases = ["aq"])
async def add_quote(ctx, userID: str, *, quote: str = None):
    if quote is None:
        await ctx.send("Please provide a quote.")
        return

    with open("quotes.json", "r") as quoteDB:
        data = json.load(quoteDB)

    for name in data["users"]:
        if userID in name["aliases"]:
            id = name["aliases"][0]

            if quote in name["quotes"]:
                await ctx.send("That quote already exists.")
                return
            else:
                name["quotes"].append(quote)
                with open("quotes.json", "w") as quoteDB:
                    json.dump(data, quoteDB)
                await ctx.send(f"Quote \"{quote}\" has been added to {id}!")
                
                # creating a dictionary for the last quote file
                lastQuoteDict = {
                    "name": id,
                    "quote": quote,
                }

                with open("lastQuote.json", "w") as lastQDB:
                    json.dump(lastQuoteDict, lastQDB)
                return
    await ctx.send(f"Sorry, {userID} not found.")

## Last Quote command
@bot.command(aliases = ["lq", "last q"])
async def last_quote(ctx):
    with open("lastQuote.json", "r") as lastQDB:
        lastQuoteDB = json.load(lastQDB)
        lastQuote = lastQuoteDB["quote"]
        lastQuoteName = lastQuoteDB["name"]

    if lastQuote != "":
        await ctx.send(f"The last quote added was: \"{lastQuote}\" from {lastQuoteName}")

    else:
        await ctx.send("No quotes have been added yet.")

## List Quote command
@bot.command(aliases=["liq", "list q"])
async def list_quotes(ctx, *, userID: str = None):
    with open("quotes.json", "r") as quoteDB:
        data = json.load(quoteDB)

    if userID is None:
        await ctx.send("Please choose a name to list quotes from.")

    else:
        for name in data["users"]:

            if userID in name["aliases"]:
                quotes = name["quotes"]

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

        await ctx.send(f"Sorry, {userID} not found.")

## Birthday command
@bot.command(aliases=["b", "bday"])
async def birthday(ctx, *, userID: str = None):
    with open ("quotes.json", "r") as birthdayDB:
        data = json.load(birthdayDB)

        if userID is None:
            # Chooses nearest birthday
            days_until_next_birthday = float('inf')
            today = datetime.today().date()

            for name in data["users"]:
                user_aliases = name.get("aliases", [])  
                userID = user_aliases[0]
                birthday_str = name.get("birthday", "")

                if birthday_str:
                    birthday = datetime.strptime(birthday_str, "%m/%d").replace(year=today.year).date()

                    # Check if the birthday is in the future
                    if birthday >= today:
                        days_until_birthday = (birthday - today).days

                        # Update if the current name has a closer birthday
                        if days_until_birthday < days_until_next_birthday:
                            days_until_next_birthday = days_until_birthday
                            next_birthday_name = userID

            if next_birthday_name:
                await ctx.send(f"The next birthday is {next_birthday_name}'s, in {days_until_next_birthday} days.")
        else:
            for name in data["users"]:

                if userID in name["aliases"]:
                    birthday = name["birthday"]

                    if birthday != "":
                        await ctx.send(f"{name['aliases'][0]}'s birthday is on {birthday}.")

                    else:
                        await ctx.send(f"Sorry, {name['aliases'][0]} doesn't have a birthday.")
                    return

            await ctx.send(f"Sorry, {userID} not found.")
        
## Bot Update command
@bot.command(aliases=["upd"])
async def update_bot(ctx, *, userID: str = None):
    	rasp.update_bot()

# Error handling    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send(f"Either the command wasn't used correctly.. || Or something is broken - (@andycap#5570) ||")
        return
    raise error
    
bot.run(TOKEN)