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
from random import randint

from discord.ext.commands import Bot
from discord_slash import SlashCommand
from termcolor import cprint, colored

from achievements import *

firstboot = 0
"""
Checking to make sure the correct config files exist
if they do not they are created with default settings
"""
if os.path.exists(os.getcwd() + "/config.json"):

    with open("./config.json") as f:
        configData = json.load(f)

else:
    configTemplate = {
        "Token": "YOUR BOT TOKEN",
        "Prefix": "PREFIX HERE",
        "Owner": "OWNER ID HERE",
        "WeatherAPIKey": "API KEY HERE",
        "Presence": {
            "Type": "watching",
            "Message": "The Weather"
        },
        "Require Auth Code For High Security Commands": True
    }

    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)

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

bot = Bot(intents=intents, command_prefix=[configData["Prefix"], "/"], self_bot=True, HelpCommand=False)
slash = SlashCommand(bot)


if configData["Token"] == "YOUR BOT TOKEN" or configData["Prefix"] == "PREFIX HERE" or configData[
        "Owner"] == "OWNER ID HERE" or configData["WeatherAPIKey"] == "API KEY HERE":
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
    """
    Syncs bots commands on startup
    """
    cprint('⚙️Loading Cogs', 'blue')
    i = os.listdir('./Cogs')
    print(i)
    for filename in i:
        if filename.endswith('.py'):
            bot.load_extension(f'Cogs.{filename[:-3]}')
            print('Loaded ' + filename)
            continue
    cprint('⚙️Syncing Commands', 'blue')
    await sync_all_commands(bot)


token = configData["Token"]
bot.run(token)
