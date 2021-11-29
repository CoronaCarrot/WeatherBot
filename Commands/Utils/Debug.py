import discord
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext
from discord_webhook import DiscordWebhook
import os
import requests

from main import bot


class Debug(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_ext.cog_slash(name="debug")
    async def _debug(self, ctx: SlashContext):
        if ctx.author.id == int(os.environ['owner']):
          api = requests.get(url="https://weatherbot.carrotgod.repl.co/api/status")
          api = api.json()
          embed = discord.Embed(title="Upstats - Server Host",
          description=f'Webserver `{api["Webserver"]}`\nBot `{api["Discord Bot"]}`',
                                                              color=0x53b9e4)
          await ctx.send(embed=embed, hidden=False)
        else:
            embed = discord.Embed(title="<:Error:764493646199521291> | Permission Error",
                                  description="Only bot developers can execute this command", color=0xf63737)
            await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Debug(bot))

