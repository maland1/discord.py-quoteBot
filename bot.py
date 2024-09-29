import json
import random
from datetime import datetime
import discord
from rasp import rasp
from discord.ext import commands
from discord.ext.commands import CommandNotFound

# Logging in and setting currently active servers
with open("env.json", "r") as env:    
    data = json.load(env)
    TOKEN = data.get("secret_key")
    GUILDS = data.get("guilds")


# Initialising bot basics
bot = commands.Bot(command_prefix=["!zzz "], intents = discord.Intents().all())


# First thing the bot does on launch
@bot.event
async def on_ready():
    print(f"{bot.user.name} reporting for duty!")


# Bot commands
## Quote command
@bot.command(aliases = ["q"])
async def quote(ctx, *, user: str = None):
    with open("quotes.json", "r") as quoteDB:
        data = json.load(quoteDB)

        if user:
            for name in data["users"]:
                if user in name["aliases"]:
                    quotes = name["quotes"]

                    if len(quotes)>0:
                        randomQuote = random.choice(quotes)
                        await ctx.send(f'"{randomQuote}" - {name["aliases"][0]}')

                    else:
                        await ctx.send(f"Sorry, {name['aliases'][0]} doesn't have any quotes.")

                    return
            await ctx.send(f"Sorry, {user} not found.")
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
async def add_quote(ctx, user: str, *, quote: str = None):
    if quote is None:
        await ctx.send("Please provide a quote.")
        return

    with open("quotes.json", "r") as quoteDB:
        data = json.load(quoteDB)

    for name in data["users"]:
        if user in name["aliases"]:
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
    await ctx.send(f"Sorry, {user} not found.")

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
async def list_quotes(ctx, *, user: str = None):
    with open("quotes.json", "r") as quoteDB:
        data = json.load(quoteDB)

    if user is None:
        await ctx.send("Please choose a name to list quotes from.")

    else:
        for name in data["users"]:

            if user in name["aliases"]:
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

        await ctx.send(f"Sorry, {user} not found.")

## Birthday commands
@bot.command(aliases=["b", "bday"])
async def birthday(ctx, *, user: str = None):
    with open ("quotes.json", "r") as birthdayDB:
        data = json.load(birthdayDB)

        if user is None:
            # Chooses nearest birthday
            days_until_next_birthday = float('inf')
            today = datetime.today().date()

            for name in data["users"]:
                user_aliases = name.get("aliases", [])  
                user = user_aliases[0]
                birthday_str = name.get("birthday", "")

                if birthday_str:
                    birthday = datetime.strptime(birthday_str, "%d/%m").replace(year=today.year).date()

                    # Check if the birthday is in the future
                    if birthday >= today:
                        days_until_birthday = (birthday - today).days

                        # Update if the current name has a closer birthday
                        if days_until_birthday < days_until_next_birthday:
                            days_until_next_birthday = days_until_birthday
                            next_birthday_name = user

            if next_birthday_name:
                await ctx.send(f"The next birthday is {next_birthday_name}'s, in {days_until_next_birthday} days.")
        else:
            for name in data["users"]:

                if user in name["aliases"]:
                    birthday_date = name.get("birthday", "")
                    
                    if birthday_date:
                        birthday = datetime.strptime(birthday_date, "%d/%m").date()
                        await ctx.send(f"{name['aliases'][0]}'s birthday is the {birthday.strftime('%d of %B').lstrip('0').replace(' 0', ' ')}.")


                    else:
                        await ctx.send(f"Sorry, {name['aliases'][0]} doesn't have a birthday.")
                    return

            await ctx.send(f"Sorry, {user} not found.")


@bot.command()
async def list_birthday(ctx):
    with open("quotes.json", "r") as birthdayDB:
        data = json.load(birthdayDB)

    return_message = ""

    for name in data["users"]:
        birthday = name.get("birthday", "")
        if birthday:
            return_message += f"{name['aliases'][0]}'s birthday is the {datetime.strptime(birthday, '%d/%m').strftime('%d of %B').lstrip('0').replace(' 0', ' ')}.\n"

    userID = name.get("id")
    print(userID)
    channel = bot.get_channel(315189684097515534)
    await channel.send(f"Happy birthday <@{userID}>!")
    await ctx.send(return_message)
        

@bot.command()
async def add_birthday(ctx, user: str, birthday: str):
    with open("quotes.json", "r") as birthdayDB:
        data = json.load(birthdayDB)

    for name in data["users"]:
        if user in name["aliases"]:
            name["birthday"] = birthday
            with open("quotes.json", "w") as birthdayDB:
                json.dump(data, birthdayDB)
            await ctx.send(f"{name['aliases'][0]}'s birthday has been set to the {datetime.strptime(birthday, '%d/%m').strftime('%d of %B').lstrip('0').replace(' 0', ' ')}.")
            return
        
    await ctx.send(f"Sorry, {user} not found.")

@bot.command()
async def send_birthday(ctx):
    with open("quotes.json", "r") as birthdayDB:
        data = json.load(birthdayDB)

    today = datetime.today().date()

    for name in data["users"]:
        userID = name.get("id")
        birthday_str = name.get("birthday", "")

        if birthday_str:
            birthday = datetime.strptime(birthday_str, "%d/%m").replace(year=today.year).date()

            if birthday == today:
                channel = bot.get_channel(315189684097515534)
                await channel.send(f"Happy birthday <@{userID}>!")
                return


## Bot Update command
@bot.command(aliases=["upd"])
async def update_bot(ctx):
    	rasp.update_bot()

# Error handling    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send("Either the command wasn't used correctly.. || Or something is broken - (@andycap#5570) ||")
        return
    raise error
    

bot.run(TOKEN)