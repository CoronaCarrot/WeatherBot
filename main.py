# -----------------------------------------------------------
# demonstrates fetching from an API and using that information
# in a discord bot environment.
#
# (C) 2021 Tyler McMullen, England
# Released under GNU Public License (GPL)
# email tyler.mcmullen.552@accesstomusic.ac.uk
# -----------------------------------------------------------
"""
Module Imports
"""
import discord
from discord.ext import commands
from termcolor import cprint, colored
import os
import time
import json
import random
from discordpy_slash.slash import *


if os.path.exists(os.getcwd() + "/config.json"):

    with open("./config.json") as f:
        configData = json.load(f)

else:
    configTemplate = {"Token": "YOUR BOT TOKEN", "Prefix": "PREFIX HERE", "Owner": "OWNER ID HERE",
                      "WeatherAPIKey": "API KEY HERE", "Presence": {"Type": "watching",
                                                                    "Message": "The Weather"}}

    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)

if os.path.exists(os.getcwd() + "/icons.json"):
    with open("./icons.json") as f:
        icondata = json.load(f)

else:
    icontemplate = {"1": "<:01:900016260304236565>",
                    "2": "<:02:900016260488765491>",
                    "3": "<:03:900016260551696384>",
                    "4": "<:04:900016260132253758>",
                    "5": "<:05:900016260551688242>",
                    "6": "<:06:900016260543311972>",
                    "7": "<:07:900016260614594580>",
                    "8": "<:08:900016260484562954>",
                    "11": "<:11:900016260480368700>",
                    "12": "<:12:900016260711063562>",
                    "13": "<:13:900016260241305641>",
                    "14": "<:14:900016260107092009>",
                    "15": "<:15:900016260421677056>",
                    "16": "<:16:900016260513923082>",
                    "17": "<:17:900016260652351530>",
                    "18": "<:18:900016260576845864>",
                    "19": "<:19:900016260119674962>",
                    "20": "<:20:900016260451020810>",
                    "21": "<:21:900016260438425610>",
                    "22": "<:22:900016260488769586>",
                    "23": "<:23:900016260635586570>",
                    "24": "<:24:900016260107100243>",
                    "25": "<:25:900016260379729962>",
                    "26": "<:26:900016260455211068>",
                    "29": "<:29:900016260430049331>",
                    "30": "<:30:900016260610420747>",
                    "31": "<:31:900016260392296478>",
                    "32": "<:32:900016260354560040>",
                    "33": "<:33:900016260392300555>",
                    "34": "<:34:900016260383920230>",
                    "35": "<:35:900016260346179614>",
                    "36": "<:36:900016260476186636>",
                    "37": "<:37:900016260107100182>",
                    "38": "<:38:900016260430065714>",
                    "39": "<:39:900016262279757844>",
                    "40": "<:40:900016260337778718>",
                    "41": "<:41:900016260383903754>",
                    "42": "<:42:900016260237111347>",
                    "43": "<:43:900016260279054378>",
                    "44": "<:44:900016260308402184>"
                    }

    with open(os.getcwd() + "/icons.json", "w+") as f:
        json.dump(icontemplate, f)

intents = discord.Intents.default()

intents.members = True

bot = commands.Bot(command_prefix=configData["Prefix"], intents=intents)


@bot.event
async def on_ready():
    print(colored("―――――――――――――――", "blue"))
    print(colored("》", "blue"), "    Weather Bot    ", colored("《", "blue"))
    print(colored("   •", "blue"), "version  0.0.1", colored("•", "blue"))
    print(colored("―――――――――――――――", "blue"))
    print()
    cprint('⚙️Syncing Commands', 'blue')
    prm = configData["Presence"]["Message"]
    if configData["Presence"]["Type"].lower == "watching":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=prm))
    elif configData["Presence"]["Type"].lower == "playing":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=prm))
    elif configData["Presence"]["Type"].lower == "listening":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=prm))
    else:
        pass
    await sync_all_commands(bot)


@bot.command()
async def resync(ctx):
    if ctx.message.author.id == 642729210368098324:
        cprint('⚙️Syncing Commands', 'blue')
        await sync_all_commands(bot)
        embed = discord.Embed(title="⚙️ | Attempting To Resync", color=0x6ba2fa)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="<:Error:764493646199521291> | Permission Error",
                              description="Only bot developers can execute this command", color=0xf63737)
        await ctx.send(embed=embed)


@bot.command()
async def weather(ctx, location):

    print(colored(f'⚠️Executing Command "Weather" For {str(ctx.message.author)}', "blue"))
    locationr = location.replace(" ", "%20")
    apikey = configData["WeatherAPIKey"]
    locationsearch = requests.get(
        f'https://dataservice.accuweather.com/locations/v1/search?apikey={apikey}&q={locationr}&language=en-us&details=true')
    responsestr = locationsearch.text
    responsejson = locationsearch.json()

    iserror = True

    if responsestr[0] == '[':
        if len(responsejson) >= 1:
            responsejson = responsejson[0]

            iserror = False

            if iserror:
                print(colored("――――――――――――――――", "blue"))
                print(colored("》", "blue"), "   Error Handling   ", colored("《", "blue"))
                print(colored("    •", "blue"), f'version 0.0.1', colored("•", "blue"))
                print()
                print(colored("Error Code » ", "blue"), f'{responsejson["Code"]}')
                print(colored("Error Message » ", "blue"), f'{responsejson["Message"]}')
                print(colored("Reference » ", "blue"), f'{responsejson["Reference"]}')
                print(colored("――――――――――――――――", "blue"))

                embed = discord.Embed(title="⚠️ | An Error Occurred", description="An error occurred while executing this command.\nCheck console for more info.", color=0xea4d65)
                embed.add_field(name=f'Error Code', value=f' `{responsejson["Code"]}`', inline=True)
                await ctx.send(embed=embed)
            else:
                locationresponse = locationsearch.json()[0]
                resultkey = locationresponse["Key"]
                weatherdata = requests.get(
                    f'https://dataservice.accuweather.com/currentconditions/v1/{resultkey}?apikey={apikey}&language=en-us&details=true')
                wdr = weatherdata.json()[0]
                tempcr = wdr["RealFeelTemperature"]["Metric"]["Value"]  # RealFeel Metric
                tempfr = wdr["RealFeelTemperature"]["Imperial"]["Value"]  # RealFeel Imperial
                tempc = wdr["Temperature"]["Metric"]["Value"]  # Temperature Metric
                tempf = wdr["Temperature"]["Imperial"]["Value"]  # Temperature Imperial
                wsm = wdr["Wind"]["Speed"]["Metric"]["Value"]  # Wind Speed Metric
                wsi = wdr["Wind"]["Speed"]["Imperial"]["Value"]  # Wind Speed Imperial
                wsd = wdr["Wind"]["Direction"]["English"]  # Wind Speed Direction
                gsi = wdr["WindGust"]["Speed"]["Imperial"]["Value"]  # Wind Gusts Imperial
                gsm = wdr["WindGust"]["Speed"]["Imperial"]["Value"]  # Wind Gusts Metric
                lube = wdr["LocalObservationDateTime"].split("T")
                lube = lube[1].split("+")
                lube = lube[0].split(":")
                if int(lube[0]) > 12:
                    lube[0] = int(lube[0]) - 12
                    lube.append("PM")
                else:
                    lube.append("AM")

                if tempc <= 5 or tempf <= 41:
                    hoc = icondata["31"]
                else:
                    hoc = icondata["30"]
                if tempcr <= 5 or tempfr <= 41:
                    hocr = icondata["31"]
                else:
                    hocr = icondata["30"]

                if wdr["WeatherIcon"] < 10:
                    pfx = f'0{wdr["WeatherIcon"]}'
                else:
                    pfx = f'{str(wdr["WeatherIcon"])}'

                icl = icondata[str(wdr["WeatherIcon"])]
                icl = icl.removeprefix(f'<:{pfx}:')
                icl = icl.replace(">", "")
                icl = f'https://cdn.discordapp.com/emojis/{icl}.png?size=2048'

                embed = discord.Embed(
                    title=f'{icondata[str(wdr["WeatherIcon"])]} It Is Currently {wdr["WeatherText"]} In {locationresponse["LocalizedName"]}',
                    color=0x53b9e4)
                embed.set_thumbnail(url=f'{icl}')
                embed.add_field(name=f'Temperature', value=f'{hoc} `{tempc}°C`', inline=True)
                embed.add_field(name=f'Feels Like', value=f'{hocr} `{tempcr}°C`', inline=True)
                embed.add_field(name=f'_ _', value=f'_ _', inline=True)

                embed.add_field(name="Wind Speeds", value=f'{icondata["32"]} `{wsd} {wsm} km/h`', inline=True)
                embed.add_field(name="Gusts", value=f'{icondata["32"]} `{gsm} km/h`', inline=True)
                embed.add_field(name=f'_ _', value=f'_ _', inline=True)
                embed.set_footer(text=f'React To Get Imperial Readings | Last Updated {lube[0]}:{lube[1]} {lube[3]}')
                await ctx.send(embed=embed)

                def check(reaction, user):
                    return user == ctx.message.author and reaction.message.author.bot

                try:
                    reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
                except asyncio.TimeoutError:
                    pass
                else:
                    edit = discord.Embed(
                        title=f'{icondata[str(wdr["WeatherIcon"])]} Imperial Readings For {locationresponse["LocalizedName"]}',
                        color=0x53b9e4)
                    edit.set_thumbnail(url=f'{icl}')
                    edit.add_field(name=f'Temperature', value=f'{hoc} `{tempf}°F`', inline=True)
                    edit.add_field(name=f'Feels Like', value=f'{hocr} `{tempfr}°F`', inline=True)
                    edit.add_field(name=f'_ _', value=f'_ _', inline=True)
                    edit.add_field(name="Wind Speeds", value=f'{icondata["32"]} `{wsd} {wsi} mi/h`', inline=True)
                    edit.add_field(name="Gusts", value=f'{icondata["32"]}  `{gsi} km/h`', inline=True)
                    edit.add_field(name=f'_ _', value=f'_ _', inline=True)
                    await ctx.send(embed=edit)
        else:
            print(colored("――――――――――――――――", "blue"))
            print(colored("》", "blue"), "   Error Handling   ", colored("《", "blue"))
            print(colored("    •", "blue"), f'version 0.0.1', colored("•", "blue"))
            print()
            print(colored("Error Code » ", "blue"), f'Index Error')
            print(colored("Error Message » ", "blue"), f'Index Out Of Range')
            print(colored("Reference » ", "blue"), f'line 127')
            print(colored("――――――――――――――――", "blue"))

            ior = discord.Embed(title="⚠️ | We Searched The World", description="Couldn't find this Town/City\nApi returned blank\nmake sure you are searching for a town/city and not a country!", color=0xea4d65)
            ior.add_field(name=f'Error Code', value=f' `UnknownLocation`', inline=True)
            await ctx.send(embed=ior)


token = configData["Token"]
bot.run(token)
