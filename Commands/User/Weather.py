import asyncio
import json.decoder

import discord
import requests
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext, ComponentContext
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from termcolor import colored

from Modules.Core.AchievementData import achievements_check
from main import configData, iconData, bot


class Weather(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_ext.cog_slash(name="weather", description="Fetch the current forecast of a Town/City")
    async def weather(self, ctx: SlashContext, location):
        locationr = location.replace(" ", "%20")  # Replace Spaces With The
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
                try:
                    wdr = weatherdata.json()[0]  # Pull JSON Data From Returned List (API Returns List)
                except json.decoder.JSONDecodeError:
                    print(weatherdata.json())
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
                    hoc = iconData["31"]  # |
                else:  # |
                    hoc = iconData["30"]  # | Checks To See If The Temperature is below 5°C or 41°F
                if tempcr <= 5 or tempfr <= 41:  # | Then Sets The Thermometer Emoji To Either Hot Or Cold
                    hocr = iconData["31"]  # |
                else:  # |
                    hocr = iconData["30"]  # |

                if wdr["WeatherIcon"] < 10:  # |
                    pfx = f'0{wdr["WeatherIcon"]}'  # | Pre Formatting For Next Section
                else:  # | Adds A Zero Before Single Digit Emoji IDs
                    pfx = f'{str(wdr["WeatherIcon"])}'  # |

                icl = iconData[str(wdr["WeatherIcon"])]  # |
                icl = icl.removeprefix(f'<:{pfx}:')  # | Converts A Discord Emoji To A PNG
                icl = icl.replace(">", "")  # | For The Embed ThumbNail
                icl = f'https://cdn.discordapp.com/emojis/{icl}.png?size=2048'  # |
                # END OF INFO GATHERING #

                """
                Pieces all the Metric information into an easy to read discord embed
                with a prompt telling the user to react to the embed (message) to receive Imperial Readings
                """
                buttons = [create_button(style=ButtonStyle.blue, label="Imperial Readings", emoji="🌦️")]
                action_row = create_actionrow(*buttons)

                embed = discord.Embed(
                    title=f'{iconData[str(wdr["WeatherIcon"])]} It Is Currently {wdr["WeatherText"]} In '
                          f'{locationresponse["LocalizedName"]}', color=0x53b9e4)
                embed.set_thumbnail(url=f'{icl}')
                embed.add_field(name=f'Temperature', value=f'{hoc} `{tempc}°C`', inline=True)
                embed.add_field(name=f'Feels Like', value=f'{hocr} `{tempcr}°C`', inline=True)
                embed.add_field(name=f'_ _', value=f'_ _', inline=True)

                embed.add_field(name="Wind Speeds", value=f'{iconData["32"]} `{wsd} {wsm} km/h`', inline=True)
                embed.add_field(name="Gusts", value=f'{iconData["32"]} `{gsm} km/h`', inline=True)
                embed.add_field(name=f'_ _', value=f'_ _', inline=True)
                embed.set_footer(
                    text=f'(C) 2021 CoronaCarrot | API Last Updated {lube[0]}:{lube[1]} {lube[3]} '
                         f'(GMT)')
                embed = await ctx.send(embed=embed, components=[action_row])
                await achievements_check(ctx, ctx.author.id, wdr, locationresponse)

                def check(msg):
                    return msg.author == ctx.author and msg.channel == ctx.channel

                unclicked = 0
                while unclicked == 0:
                    try:
                        button_ctx: ComponentContext = await wait_for_component(bot, components=action_row, timeout=30, check=check)
                        """
                            Pieces all the Imperial information into an easy to read discord embed
                            And either edits the Embed (slash command based) or sends a new embed (Prefix Based)
                            to show that new information
                            """
                        buttons = [create_button(style=ButtonStyle.success, label="Imperial Readings", emoji="🌦️",
                                                 disabled=True)]
                        action_met = create_actionrow(*buttons)

                        edit = discord.Embed(
                            title=f'{iconData[str(wdr["WeatherIcon"])]} It Is Currently {wdr["WeatherText"]} In '
                                  f'{locationresponse["LocalizedName"]}', color=0x53b9e4)
                        edit.set_thumbnail(url=f'{icl}')
                        edit.add_field(name=f'Temperature', value=f'{hoc} `{tempf}°F`', inline=True)
                        edit.add_field(name=f'Feels Like', value=f'{hocr} `{tempfr}°F`', inline=True)
                        edit.add_field(name=f'_ _', value=f'_ _', inline=True)
                        edit.add_field(name="Wind Speeds", value=f'{iconData["32"]} `{wsd} {wsi} mi/h`', inline=True)
                        edit.add_field(name="Gusts", value=f'{iconData["32"]}  `{gsi} km/h`', inline=True)
                        edit.add_field(name=f'_ _', value=f'_ _', inline=True)
                        edit.set_footer(
                            text=f'(C) 2021 CoronaCarrot | API Last Updated {lube[0]}:{lube[1]} {lube[3]} (GMT)')
                        await button_ctx.edit_origin(content="Showing Imperial Readings.", embed=edit, components=[action_met])

                    except asyncio.TimeoutError:
                        buttons = [create_button(style=ButtonStyle.blue, label="Imperial Readings", emoji="🌦️",
                                                 disabled=True)]
                        action_row = create_actionrow(*buttons)
                        await embed.edit(components=[action_row])

            else:
                """
                This is executed if the API does not find a Town/City
                it sends a discord embed indicating to the player that their search was a fail
                and advises them to make sure they have searched for a Town/City and not a country
                """
                ior = discord.Embed(title=f"We Couldn't Find This Town/City!",
                                    description="Try Searching For Town/City And Not Country", color=0xea4d65)
                await ctx.send(embed=ior)
        else:
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

            embed = discord.Embed(title="⚠️ | An Error Occurred",
                                  description="An error occurred while executing "
                                              "this command.\nCheck console for "
                                              "more info.", color=0xea4d65)
            embed.add_field(name=f'Error Code', value=f' `{responsejson["Code"]}`', inline=True)
            await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Weather(bot))
