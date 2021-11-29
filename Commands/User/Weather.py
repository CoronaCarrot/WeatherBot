import asyncio

import discord
import requests
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext, ComponentContext
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from termcolor import colored

from Modules.Core.AchievementData import achievements_check, error_ach
from main import configData, iconData, bot


class Weather(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_ext.cog_slash(name="weather", description="Fetch the current forecast of a Town/City")
    async def weather(self, ctx: SlashContext, location):
        locationr = location.replace(" ", "%20")  # Replace Spaces With The
        apikey = configData["WeatherAPIKey"]  # Pull API Key From Config
        if configData["WeatherAPIKey"]["KeyType"].lower == "premium":
            weatherdatametric = requests.get(
                f'https://pro.openweathermap.org/data/2.5/weather?q={locationr}&appid={apikey["API Key"]}&units=metric')  # Request Weather Data For Found Town/City
            weatherdataimperial = requests.get(
                f'https://pro.openweathermap.org/data/2.5/weather?q={locationr}&appid={apikey["API Key"]}&units=imperial')
        else:
            weatherdatametric = requests.get(
                f'https://api.openweathermap.org/data/2.5/weather?q={locationr}&appid={apikey["API Key"]}&units=metric')  # Request Weather Data For Found Town/City
            weatherdataimperial = requests.get(
                f'https://api.openweathermap.org/data/2.5/weather?q={locationr}&appid={apikey["API Key"]}&units=imperial')

        responsejson = weatherdatametric.json()  # Returns JSON Output From API
        print(responsejson["cod"])
        print(responsejson)
        if responsejson["cod"] not in ["401", "404", 401]:
            """
            The section of code between "# START OF INFO GATHERING #" and "# END OF INFO GATHERING #"
            takes information out of the code and puts them into separate variables to be used for discord embeds
            It also has logic that checks information to tell the bot what emojis to use next to certain info
            EG - The thermometer emoji will show as cold if the temperature is below 5°C or 41°F
            """
            # START OF INFO GATHERING #
            wdrm = weatherdatametric.json()  # Pull Metric JSON Data From Returned List (API Returns List)
            wdri = weatherdataimperial.json()
            tempcr = wdrm["main"]["feels_like"]  # RealFeel Metric
            tempfr = wdri["main"]["feels_like"]  # RealFeel Imperial
            tempc = wdrm["main"]["temp"]  # Temperature Metric
            tempf = wdri["main"]["temp"]  # Temperature Imperial
            wsm = wdrm["wind"]["speed"]  # Wind Speed Metric
            wsi = wdri["wind"]["speed"]  # Wind Speed Imperial

            if tempc <= 5 or tempf <= 41:  # |
                hoc = iconData["icons"]["31"]  # |
            else:  # |
                hoc = iconData["icons"]["30"]  # | Checks To See If The Temperature is below 5°C or 41°F
            if tempcr <= 5 or tempfr <= 41:  # | Then Sets The Thermometer Emoji To Either Hot Or Cold
                hocr = iconData["icons"]["31"]  # |
            else:  # |
                hocr = iconData["icons"]["30"]  # |

            pfx = f'{str(wdri["weather"][0]["icon"])}'  # |

            icl = f'https://openweathermap.org/img/wn/{wdri["weather"][0]["icon"]}@4x.png'  # |
            # END OF INFO GATHERING #

            """
            Pieces all the Metric information into an easy to read discord embed
            with a prompt telling the user to react to the embed (message) to receive Imperial Readings
            """
            buttons = [create_button(style=ButtonStyle.blue, label="Imperial Readings", emoji="🌦️")]
            action_row = create_actionrow(*buttons)

            embed = discord.Embed(
                title=f'{iconData["icons"][str(wdri["weather"][0]["icon"])]} Weather for {wdri["name"]}, {wdri["sys"]["country"]}', description=f'{wdri["weather"][0]["description"]}', color=0x53b9e4)
            embed.set_thumbnail(url=f'{icl}')
            embed.add_field(name=f'Temperature', value=f'{hoc} `{tempc}°C`', inline=True)
            embed.add_field(name=f'Feels Like', value=f'{hocr} `{tempcr}°C`', inline=True)
            embed.add_field(name=f'_ _', value=f'_ _', inline=True)

            embed.add_field(name="Wind Speeds", value=f'{iconData["icons"]["32"]} `{wsm} m/s`', inline=True)
            embed.add_field(name=f'_ _', value=f'_ _', inline=True)
            embed.set_footer(
                text=f'(C) 2021 CoronaCarrot | Version 2.0'
                     f'(GMT)')
            embed = await ctx.send(embed=embed, components=[action_row])
            await achievements_check(ctx, ctx.author.id, wdri, wdrm)

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel

            unclicked = 0
            while unclicked == 0:
                try:
                    button_ctx: ComponentContext = await wait_for_component(bot, components=action_row, timeout=30,
                                                                            check=check)
                    """
                            Pieces all the Imperial information into an easy to read discord embed
                            And either edits the Embed (slash command based) or sends a new embed (Prefix Based)
                            to show that new information
                            """
                    buttons = [create_button(style=ButtonStyle.success, label="Imperial Readings", emoji="🌦️",
                                             disabled=True)]
                    action_met = create_actionrow(*buttons)

                    edit = discord.Embed(
                        title=f'{iconData["icons"][str(wdri["weather"][0]["icon"])]} {wdri["name"]}, {wdri["sys"]["country"]} | {wdri["weather"][0]["description"]}', color=0x53b9e4)
                    edit.set_thumbnail(url=f'{icl}')
                    edit.add_field(name=f'Temperature', value=f'{hoc} `{tempf}°F`', inline=True)
                    edit.add_field(name=f'Feels Like', value=f'{hocr} `{tempfr}°F`', inline=True)
                    edit.add_field(name=f'_ _', value=f'_ _', inline=True)

                    edit.add_field(name="Wind Speeds", value=f'{iconData["icons"]["32"]} `{wsi} km/h`', inline=True)
                    edit.add_field(name=f'_ _', value=f'_ _', inline=True)
                    edit.set_footer(
                        text=f'(C) 2021 CoronaCarrot | Version 2.0'
                             f'(GMT)')
                    await button_ctx.edit_origin(content="Showing Imperial Readings.", embed=edit,
                                                 components=[action_met])

                except asyncio.TimeoutError:
                    buttons = [create_button(style=ButtonStyle.blue, label="Imperial Readings", emoji="🌦️",
                                             disabled=True)]
                    action_row = create_actionrow(*buttons)
                    await embed.edit(components=[action_row])

        else:
            """
            Sends an error handling message if there is an error with the API call
            Added mainly to catch the error sent when the APIs limit of 50 calls per day has been reached

            This section also sends a discord embed to the player informing them of the error,
            telling them (Or The Developer) to check console and providing an error code
            """
            if responsejson["message"] == "city not found":
                """
                This is executed if the API does not find a Town/City
                it sends a discord embed indicating to the player that their search was a fail
                and advises them to make sure they have searched for a Town/City and not a country
                """
                ior = discord.Embed(title=f"We Couldn't Find This Town/City!",
                                    description="Try Searching For Town/City And Not Country", color=0xea4d65)
                await ctx.send(embed=ior)
                await error_ach(ctx)
            else:
                print(responsejson)
                print(colored("――――――――――――――――", "blue"))
                print(colored("》", "blue"), "   Error Handling   ", colored("《", "blue"))
                print(colored("    •", "blue"), f'version 0.0.1', colored("•", "blue"))
                print()
                print(colored("Error Code » ", "blue"), f'{responsejson["cod"]}')
                print(colored("Error Message » ", "blue"), f'{responsejson["message"]}')
                print(colored("――――――――――――――――", "blue"))

                embed = discord.Embed(title="⚠️ | An Error Occurred",
                                      description="An error occurred while executing "
                                                  "this command.\nCheck console for "
                                                  "more info.", color=0xea4d65)
                embed.add_field(name=f'Error Code', value=f' `{responsejson["cod"]}`', inline=True)
                await ctx.send(embed=embed)
                await error_ach(ctx)


def setup(bot: Bot):
    bot.add_cog(Weather(bot))
