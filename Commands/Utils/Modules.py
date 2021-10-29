import discord
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice


class Debug(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_ext.cog_slash(name="command", description="manage the current command modules", options=[create_option(
        name="subcommand",
        description="List OF Subcommands For This Command",
        option_type=3,
        required=False,
        choices=[
            create_choice(
                name="list",
                value="List All Command"
            ),
            create_choice(
                name="Enable",
                value="Enable A Command"
            ),
            create_choice(
                name="Disable",
                value="Disable A Command"
            )
        ]
    )
    ])
    async def _debug(self, ctx: SlashContext):
        if ctx.author.id == 642729210368098324:
            embed = discord.Embed(title="Command Context", description="**Command** `/command`", color=0x53b9e4)
            embed.add_field(name="Usage",
                            value="`/command list` - **List All Commands**\n`/command enable <command>` - **Enables A Command**\n`/command disable <command>` - **Disables A Command**\n",
                            inline=False)
            await ctx.send(embed=embed, hidden=True)
        else:
            embed = discord.Embed(title="<:Error:764493646199521291> | Permission Error",
                                  description="Only bot developers can execute this command", color=0xf63737)
            await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Debug(bot))
