import asyncio

import discord
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext, ComponentContext
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow, \
    wait_for_component

from main import bot


class Help(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_ext.cog_slash(name="help")
    async def _help(self, ctx: SlashContext):
        select = create_select(
            options=[  # the options in your dropdown
                create_select_option("User Commands", value="ucmds", emoji="👤"),
                create_select_option("Dev Commands", value="dcmds", emoji="💻"),
            ],
            placeholder="Filter = None",  # the placeholder text to show when no options have been chosen
            min_values=1,  # the minimum number of options a user must select
            max_values=2,  # the maximum number of options a user can select
        )
        action_row = create_actionrow(select)

        help = discord.Embed(title="Bot Commands",
                             description="All commands have the / prefix and have auto-completion", color=0x53b9e4)
        help.add_field(name=f'/Weather `Location`', value=f'Fetches The Current Weather For A Location, Based On Your '
                                                          f'Search.', inline=False)
        help.add_field(name=f'/Help', value=f'Sends This Message', inline=False)
        help.add_field(name=f'/debug **[DEV]**', value=f'Fetches UpStats for the bot. Used for debugging the host and '
                                                       f'bad ping.', inline=False)
        help.add_field(name=f'/antisteal **[DEV]**', value=f'This Is A Secret :smirk:', inline=False)
        edit = await ctx.send(embed=help, components=[action_row])

        loop = True
        while loop:
            try:
                select_ctx: ComponentContext = await wait_for_component(bot, components=[action_row], timeout=30)
                #await select_ctx.defer(ignore=True)
                print(select_ctx.selected_options)
                if select_ctx.selected_options == ['ucmds']:

                    select = create_select(
                        options=[  # the options in your dropdown
                            create_select_option("User Commands", value="ucmds", emoji="👤"),
                            create_select_option("Dev Commands", value="dcmds", emoji="💻"),
                        ],
                        placeholder="Filter = User Commands",
                        # the placeholder text to show when no options have been chosen
                        min_values=1,  # the minimum number of options a user must select
                        max_values=2,  # the maximum number of options a user can select
                    )
                    action_row = create_actionrow(select)

                    filtu = discord.Embed(title="Bot Commands",
                                          description="All commands have the / prefix and have auto-completion",
                                          color=0x53b9e4)
                    filtu.add_field(name=f'/Weather `Location`',
                                    value=f'Fetches The Current Weather For A Location, Based On Your '
                                          f'Search.', inline=False)
                    filtu.add_field(name=f'/Help', value=f'Sends This Message', inline=False)
                    await edit.edit(embed=filtu, components=[action_row])
                    #await select_ctx.edit_origin(content="Cumu")
                elif select_ctx.selected_options == ['dcmds']:
                    #select_ctx.responded = True

                    select = create_select(
                        options=[  # the options in your dropdown
                            create_select_option("User Commands", value="ucmds", emoji="👤"),
                            create_select_option("Dev Commands", value="dcmds", emoji="💻"),
                        ],
                        placeholder="Filter = Dev Commands",
                        # the placeholder text to show when no options have been chosen
                        min_values=1,  # the minimum number of options a user must select
                        max_values=2,  # the maximum number of options a user can select
                    )
                    action_row = create_actionrow(select)

                    filtd = discord.Embed(title="Bot Commands",
                                          description="All commands have the / prefix and have auto-completion",
                                          color=0x53b9e4)
                    filtd.add_field(name=f'/debug **[DEV]**',
                                    value=f'Fetches UpStats for the bot. Used for debugging the host and '
                                          f'bad ping.', inline=False)
                    filtd.add_field(name=f'/antisteal **[DEV]**', value=f'This Is A Secret :smirk:', inline=False)
                    await edit.edit(embed=filtd, components=[action_row])
                    #await select_ctx.edit_origin(content="Cumd")
                elif select_ctx.selected_options == ['ucmds', 'dcmds'] or select_ctx.selected_options == ['dcmds',
                                                                                                          'ucmds']:
                    #select_ctx.responded = True

                    select = create_select(
                        options=[  # the options in your dropdown
                            create_select_option("User Commands", value="ucmds", emoji="👤"),
                            create_select_option("Dev Commands", value="dcmds", emoji="💻"),
                        ],
                        placeholder="Filter = None",  # the placeholder text to show when no options have been chosen
                        min_values=1,  # the minimum number of options a user must select
                        max_values=2,  # the maximum number of options a user can select
                    )
                    action_row = create_actionrow(select)

                    filtn = discord.Embed(title="Bot Commands",
                                          description="All commands have the / prefix and have auto-completion",
                                          color=0x53b9e4)
                    filtn.add_field(name=f'/Weather `Location`',
                                    value=f'Fetches The Current Weather For A Location, Based On Your '
                                          f'Search.', inline=False)
                    filtn.add_field(name=f'/Help', value=f'Sends This Message', inline=False)
                    filtn.add_field(name=f'/debug **[DEV]**',
                                    value=f'Fetches UpStats for the bot. Used for debugging the host and '
                                          f'bad ping.', inline=False)
                    filtn.add_field(name=f'/antisteal **[DEV]**', value=f'This Is A Secret :smirk:', inline=False)
                    await edit.edit(embed=filtn, components=[action_row])
                    #await select_ctx.edit_origin(content="Cuma")
                await select_ctx.defer(ignore=True)
            except asyncio.TimeoutError:
                select = create_select(
                    options=[  # the options in your dropdown
                        create_select_option("ucmds", value="User Commands", emoji="👤"),
                        create_select_option("dcmds", value="Dev Commands", emoji="💻"),
                    ],
                    placeholder="Filter = None",  # the placeholder text to show when no options have been chosen
                    min_values=1,  # the minimum number of options a user must select
                    max_values=2,  # the maximum number of options a user can select
                    disabled=True,
                )
                action_row = create_actionrow(select)

                await edit.edit(components=[action_row])
                loop = False


def setup(bot: Bot):
    bot.add_cog(Help(bot))