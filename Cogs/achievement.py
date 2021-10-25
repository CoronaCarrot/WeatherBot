import discord
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext

from achievements import achievements_logic


class Slash(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_ext.cog_slash(name="achievements")
    async def _achievements(self, ctx: SlashContext):
        achlogic = await achievements_logic(ctx)
        embed = discord.Embed(title="{users}'s Achievements",
                              description=f'All unlocked achievement badges\non this bot. Use `/achievement ID`\nfor sp'
                                          f'ecific achievement information.\n\n{achlogic}',
                              color=0x53b9e4)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="achievement")
    async def _achievement(self, ctx: SlashContext, ID):
        pass


def setup(bot: Bot):
    bot.add_cog(Slash(bot))