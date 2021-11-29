# -----------------------------------------------------------
# demonstrates fetching from an API and using that information
# in a discord bot environment.
#
# (C) 2021 CoronaCarrot
# Released under GNU Public License (GPL)
# email wae375@outlook.com
# -----------------------------------------------------------
"""
Module Imports
"""
import time
from random import randint

import requests
from termcolor import cprint, colored

from Modules.Core.AchievementData import *

firstboot = 0
"""
Checking to make sure the correct config files exist
if they do not they are created with default settings
"""
if os.path.exists("./config.json"):

    with open("./config.json") as f:
        configData = json.load(f)

else:
    configTemplate = {
        "Token": "YOUR BOT TOKEN",
        "Owner": "OWNER ID HERE",
        "WeatherAPIKey": {
            "KeyType": "FREE/PREMIUM",
            "API Key": "API KEY HERE"
        },
        "Presence": {
            "Type": "watching",
            "Message": "The Weather"
        },
        "Require Auth Code For High Security Commands": True
    }

    with open(os.getcwd() + "./config.json", "w+") as f:
        json.dump(configTemplate, f, indent=4, sort_keys=True)

    print(colored("―――――――――――――――", "blue"))  # |
    print(colored("》", "blue"), "    Weather Bot    ", colored("《", "blue"))  # | Sends Bot branding to console
    print(colored("   •", "blue"), "version  0.0.1", colored("•", "blue"))  # | and sends version info
    print(colored("―――――――――――――――", "blue"))  # |
    print()
    cprint('⚙️Beginning First Boot Setup', 'blue')  # Sends in console that the bot is beginning first time setup
    time.sleep(randint(0, 3))  # Pause For Effect
    cprint('⚙️Creating Config Files', 'blue')  # Sends in console that the bot is creating config files
    time.sleep(randint(0, 3))  # Pause For Effect
    with open("./config.json") as f:
        configData = json.load(f)
    firstboot = 1

if os.path.exists(os.getcwd() + "./icons.json"):
    with open("./icons.json") as f:
        iconData = json.load(f)

else:
    icontemplate = {"icons": {
        "30": "<:30:900016260610420747>",
        "31": "<:31:900016260392296478>",
        "32": "<:32:900016260354560040>",
        "01d": "<:01d:905217837025624084>",
        "01n": "<:01n:905217837260505178>",
        "02d": "<:02d:905217837126266961>",
        "02n": "<:02n:905217837013041222>",
        "03d": "<:03d:905217837021401149>",
        "03n": "<:03n:905217836958494761>",
        "04d": "<:04d:905217837138866176>",
        "04n": "<:04n:905217836656504883>",
        "09d": "<:09d:905217837117898762>",
        "09n": "<:09n:905217836966887424>",
        "10d": "<:10d:905217836736184341>",
        "10n": "<:10n:905217837210173470>",
        "11d": "<:11d:905217836945899590>",
        "11n": "<:11n:905217836513902653>",
        "13d": "<:13d:905217836937535498>",
        "13n": "<:13n:905217836652306443>",
        "50d": "<:50d:905217837033996308>",
        "50n": "<:50n:905217837033996338>",
    },
        "descriptions": {
            "unset": "unset"
        }}

    with open(os.getcwd() + "./icons.json", "w+") as f:
        json.dump(icontemplate, f, indent=4, sort_keys=True)

intents = discord.Intents.default()

intents.members = True

bot = Bot(intents=intents, command_prefix="/", self_bot=True)
slash = SlashCommand(bot)

"""
Syncs bots commands on startup
"""
i = os.listdir('./Commands')
cogs = 0
for filename in i:
    if filename.endswith('.py'):
        bot.load_extension(f'Commands.{filename[:-3]}')
        cogs += 1
    elif os.path.isdir(f'./Commands/{filename}'):
        o = os.listdir(f'./Commands/{filename}')
        for incat in o:
            if incat.endswith('.py'):
                cogs += 1
                bot.load_extension(f'Commands.{filename}.{incat[:-3]}')

if configData["Token"] == "YOUR BOT TOKEN" or configData[
    "Owner"] == "OWNER ID HERE" or configData["WeatherAPIKey"]["API Key"] == "API KEY HERE" or \
        configData["WeatherAPIKey"]["KeyType"] == "FREE/PREMIUM":
    if firstboot == 1:
        pass
    else:
        print(colored("―――――――――――――――", "blue"))  # |
        print(colored("》", "blue"), "    Weather Bot    ", colored("《", "blue"))  # | Sends Bot branding to console
        print(colored("   •", "blue"), "version  0.0.1", colored("•", "blue"))  # | and sends version info
        print(colored("―――――――――――――――", "blue"))  # |
    print()
    print(colored("――――――――――――――――", "blue"))
    print(colored("》", "blue"), "   Error Handling   ", colored("《", "blue"))
    print(colored("    •", "blue"), f'version 0.0.1', colored("•", "blue"))
    print()
    print(colored("Error Code » ", "blue"), f'ConfigError')
    print(colored("Error Message » ", "blue"), f'Detected Unedited Config. Please Setup Config Before Running This Bot')
    print(colored("Reference » ", "blue"), f'config.json')
    print(colored("――――――――――――――――", "blue"))
    exit(0)
else:
    pass

"""
All events ran on startup
"""


@bot.event
async def on_ready():
    if firstboot == 1:
        pass
    else:
        print(colored("―――――――――――――――", "blue"))  # |
        print(colored("》", "blue"), "    Weather Bot    ", colored("《", "blue"))  # | Sends Bot branding to console
        print(colored("   •", "blue"), "version  0.0.1", colored("•", "blue"))  # | and sends version info
        print(colored("―――――――――――――――", "blue"))  # |
    print()
    global cogs
    cprint(f'⚙️Loaded {cogs} Commands', 'blue')
    try:
        await slash.sync_all_commands()
        cprint('⚙️Syncing Commands', 'blue')
    except discord.errors.HTTPException:
        cprint('⚙️An Error Occurred During Command Sync - could be a rate limit', 'blue')
    cprint('⚙️Accepting Commands', 'blue')  # Sends in console that the bot is now excepting discord commands
    """
    Sets the bots status in discord depending on the information given in the config
    """
    prm = configData["Presence"]["Message"]  # Gets Status Message From Config
    if str(configData["Presence"]["Type"]).lower() == "watching":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=prm))
        cprint(f'⚙️Set Status To "Watching {prm}"', 'blue')
    elif str(configData["Presence"]["Type"]).lower() == "playing":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=prm))
        cprint(f'⚙️Set Status To "Playing {prm}"', 'blue')
    elif str(configData["Presence"]["Type"]).lower() == "listening":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=prm))
        cprint(f'⚙️Set Status To "Listening to {prm}"', 'blue')
    else:
        pass


@bot.event
async def on_command_error(ctx, error):
    await error_ach(ctx)


token = configData["Token"]
try:
    request = requests.get("https://youtu.be/dQw4w9WgXcQ", timeout=15)
    if bot.is_ws_ratelimited():
        print(colored("―――――――――――――――", "blue"))  # |
        print(colored("》", "blue"), "    Weather Bot    ", colored("《", "blue"))  # | Sends Bot branding to console
        print(colored("   •", "blue"), "version  0.0.1", colored("•", "blue"))  # | and sends version info
        print(colored("―――――――――――――――", "blue"))  # |
        print()
        print(colored("Cannot start bot. Could be rate limited.", "blue"))
        exit(0)
    else:
        try:
            bot.run(token)
        except all:
            print(colored("―――――――――――――――", "blue"))  # |
            print(colored("》", "blue"), "    Weather Bot    ", colored("《", "blue"))  # | Sends Bot branding to console
            print(colored("   •", "blue"), "version  0.0.1", colored("•", "blue"))  # | and sends version info
            print(colored("―――――――――――――――", "blue"))  # |
            print()
            print(colored("Cannot start bot. Couldn't detect any possible reasons.", "blue"))
            exit(0)
except (requests.ConnectionError, requests.Timeout) as exception:
    print(colored("―――――――――――――――", "blue"))  # |
    print(colored("》", "blue"), "    Weather Bot    ", colored("《", "blue"))  # | Sends Bot branding to console
    print(colored("   •", "blue"), "version  0.0.1", colored("•", "blue"))  # | and sends version info
    print(colored("―――――――――――――――", "blue"))  # |
    print()
    print(colored(
        "Cannot start bot.\nYou are either not connected to the internet\nor your ping is so high that it takes more tha"
        "n 15 seconds to load a webpage...\n\nif the cause is option two GET THE FUCK OUT OF MCDONALDS...",
        "blue"))
    exit(0)
