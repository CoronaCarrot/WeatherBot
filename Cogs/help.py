import discord
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext


class Slash(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_ext.cog_slash(name="help")
    async def _help(self, ctx: SlashContext):
        help = discord.Embed(title="Bot Commands",
                             description="All commands have the / prefix and have auto-completion", color=0x53b9e4)
        help.add_field(name=f'/Weather `Location`', value=f'Fetches The Current Weather For A Location, Based On Your '
                                                          f'Search.', inline=False)
        help.add_field(name=f'/Help', value=f'Sends This Message', inline=False)
        help.add_field(name=f'/debug **[DEV]**', value=f'Fetches UpStats for the bot. Used for debugging the host and '
                                                       f'bad ping.', inline=False)
        help.add_field(name=f'/antisteal **[DEV]**', value=f'This Is A Secret :smirk:', inline=False)
        await ctx.send(embed=help)


def setup(bot: Bot):
    bot.add_cog(Slash(bot))
