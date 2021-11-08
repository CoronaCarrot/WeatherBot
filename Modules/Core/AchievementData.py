import datetime
import json
import os

import discord
from discord import Intents
from discord.ext.commands import Bot
from discord_slash import SlashCommand

intents = Intents.default()

intents.members = True

if os.path.exists("../../config.json"):

    with open("../../config.json") as f:
        configData = json.load(f)

    bot = Bot(intents=intents, command_prefix=[configData["Prefix"], "/"], self_bot=True)
    slash = SlashCommand(bot)

else:
    bot = Bot(intents=intents, command_prefix=["/"], self_bot=True)
    slash = SlashCommand(bot)

if os.path.exists("achievements_config.json"):

    with open("achievements_config.json") as f:
        achdata = json.load(f)

else:

    achtemp = {"01": {
            "Name": "Noice",
            "Description": "Get a temperature of 69° Fahrenheit",
            "Rarity": "Rare",
            "Icon": "<:01:901465545075986513>"
        },
        "02": {
            "Name": "Birthplace",
            "Description": "Fetch the weather of the bots birthplace",
            "Rarity": "Special",
            "Icon": "<:02:901468443314901042>"
        },
        "03": {
            "Description": "Dm the bot. *Why?* *Just... Why?*",
            "Icon": "<:03:901468444355100682>",
            "Name": "What a conversation",
            "Rarity": "Special"
        }
    }

    with open("achievements_config.json", 'w+') as f:
        json.dump(achtemp, f, indent=4, sort_keys=True)

    with open("achievements_config.json") as f:
        achdata = json.load(f)


async def achievements_check(ctx, user, wdri, wdrm):
    file = "./UserData/{0}.json".format(str(user))

    user = bot.get_user(ctx.author.id)
    if os.path.exists(os.getcwd() + file):

        with open(file) as f:
            userdata = json.load(f)

    else:

        usertemp = {
            "ID": ctx.author.id,
            "Achievements": {
                "01": {
                    "Achieved": False,
                    "Date Achieved": ""
                },
                "02": {
                    "Achieved": False,
                    "Date Achieved": ""
                },
                "03": {
                    "Achieved": False,
                    "Date Achieved": ""
                }
            }
        }

        with open(os.getcwd() + file, 'w+') as f:
            json.dump(usertemp, f, indent=4, sort_keys=True)

        with open(file) as f:
            userdata = json.load(f)
    if int(wdri["main"]["temp"]) // 1 == 69:
        if userdata["Achievements"]["01"]["Achieved"]:
            pass
        else:
            userdata["Achievements"]["01"]["Achieved"] = True
            userdata["Achievements"]["01"]["Date Achieved"] = f'{datetime.datetime.now()}'

            ach01 = discord.Embed(title=f"Achievement Unlocked | {achdata['01']['Name']}",
                                  description=f"{achdata['01']['Description']}",
                                  color=0x53b9e4)
            ach01.set_thumbnail(url="https://cdn.discordapp.com/emojis/901465545075986513.png?size=64")
            await ctx.send(embed=ach01)
    if wdri["name"] == "Norwich":
        if userdata["Achievements"]["02"]["Achieved"]:
            pass
        else:
            userdata["Achievements"]["02"]["Achieved"] = True
            userdata["Achievements"]["02"]["Date Achieved"] = f'{datetime.datetime.now()}'

            ach01 = discord.Embed(title=f"Achievement Unlocked | {achdata['02']['Name']}",
                                  description=f"{achdata['02']['Description']}", color=0x53b9e4)
            ach01.set_thumbnail(url="https://cdn.discordapp.com/emojis/901468443314901042.png?size=64")
            await ctx.channel.send(embed=ach01)

    with open(os.getcwd() + file, 'w+') as f:
        json.dump(userdata, f, indent=4, sort_keys=True)


async def badge_board(ctx):
    file = "./UserData/{0}.json".format(str(ctx.author.id))

    user = bot.get_user(ctx.author.id)
    if os.path.exists(os.getcwd() + file):

        with open(file) as f:
            userdata = json.load(f)

    else:

        usertemp = {
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

        with open(file, 'w+') as f:
            json.dump(usertemp, f, indent=4, sort_keys=True)

        with open(file) as f:
            userdata = json.load(f)

    tablec = 0
    table = ""
    for (key, value) in userdata["Achievements"].items():
        tablec += 1
        if dict(value)["Achieved"]:
            table = table + str(achdata[str(key)]["Icon"])
        else:
            if achdata[str(key)]["Rarity"] == "Special":
                table = table + "<:locked_special:901465836433326110>"
            else:
                table = table + "<:locked:901491003838591018>"
        if tablec >= 10:
            tablec = 0
            table = table + "\n\n"
        else:
            pass
    return table
