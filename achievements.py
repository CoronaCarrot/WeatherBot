import datetime
import json
import os

import discord
from discord import Intents
from discord.ext.commands import Bot
from discord_slash import SlashCommand

if os.path.exists(os.getcwd() + "/config.json"):

    with open("./config.json") as f:
        configData = json.load(f)
else:
    pass

intents = Intents.default()

intents.members = True

bot = Bot(intents=intents, command_prefix=[configData["Prefix"], "/"], self_bot=True, HelpCommand=False)
slash = SlashCommand(bot)


async def achievements_check(ctx, user, wdr, locationresponse):
    file = "./UserData/{0}.json".format(str(user))

    user = bot.get_user(ctx.author.id)
    if os.path.exists(os.getcwd() + file):

        with open(file) as f:
            achdata = json.load(f)

    else:

        achtemp = {
            "ID": ctx.author.id,
            "Achievements": {
                "01": {
                    "Achieved": False,
                    "Date Achieved": ""
                },
                "02": {
                    "Achieved": False,
                    "Date Achieved": ""
                }
            }
        }

        with open(os.getcwd() + file, 'w+') as f:
            json.dump(achtemp, f)

        with open(file) as f:
            achdata = json.load(f)

    if wdr["Temperature"]["Imperial"]["Value"] == 69.0:
        if achdata["Achievements"]["01"]["Achieved"]:
            pass
        else:
            achdata["Achievements"]["01"]["Achieved"] = True
            achdata["Achievements"]["01"]["Date Achieved"] = f'{datetime.datetime.now()}'

            ach01 = discord.Embed(title="Achievement Unlocked | Noice",
                                  description="Get a temperature of 69° Fahrenheit",
                                  color=0x53b9e4)
            ach01.set_thumbnail(url="https://cdn.discordapp.com/emojis/901465545075986513.png?size=64")
            await ctx.send(embed=ach01)
    if locationresponse["LocalizedName"] == "Norwich":
        if achdata["Achievements"]["02"]["Achieved"]:
            pass
        else:
            achdata["Achievements"]["02"]["Achieved"] = True
            achdata["Achievements"]["02"]["Date Achieved"] = f'{datetime.datetime.now()}'

            ach01 = discord.Embed(title="Achievement Unlocked | Birthplace", description="Fetch the weather of the "
                                                                                         "bots birthplace",
                                  color=0x53b9e4)
            ach01.set_thumbnail(url="https://cdn.discordapp.com/emojis/901468443314901042.png?size=64")
            await ctx.channel.send(embed=ach01)

    with open(os.getcwd() + file, 'w+') as f:
        json.dump(achdata, f)


async def achievements_logic(ctx):
    file = "./UserData/{0}.json".format(str(ctx.author.id))

    user = bot.get_user(ctx.author.id)
    if os.path.exists(os.getcwd() + file):

        with open(file) as f:
            achdata = json.load(f)

    else:

        achtemp = {
            "ID": ctx.author.id,
            "Achievements": {
                "01": {
                    "Achieved": False,
                    "Date Achieved": ""
                },
                "02": {
                    "Achieved": False,
                    "Date Achieved": ""
                }
            }
        }

        with open(os.getcwd() + file, 'w+') as f:
            json.dump(achtemp, f)

        with open(file) as f:
            achdata = json.load(f)

    for x in achdata["Achievements"]:
        print(x)
