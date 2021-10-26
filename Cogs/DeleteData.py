import asyncio
import base64
import os
import uuid

import discord
import pyotp
import qrcode
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext, ButtonStyle, ComponentContext
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component

from main import configData, bot


class DeleteData(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_ext.cog_slash(name="deletedata")
    async def _deletedata(self, ctx: SlashContext, user=None):
        if ctx.author.id == 642729210368098324:
            if type(user) == str and str(user).lower() == "all":
                buttons = [create_button(style=ButtonStyle.blurple, label="Yes", emoji="✅", custom_id="Yes"),
                           create_button(style=ButtonStyle.blurple, label="No", emoji="❌", custom_id="No")]
                action_row = create_actionrow(*buttons)

                embed = discord.Embed(title="⚙️ | Are You Sure?",
                                      description=f'This will delete **ALL** user\ndata registered to this bot.\nDo you wish'
                                                  f' to continue?', color=0xf63737)
                edit = await ctx.send(embed=embed, components=[action_row], hidden=True)

                def check(ctx: ComponentContext):
                    return ctx.author == ctx.author and ctx.channel == ctx.channel and ctx.component_id in ["Yes", "No"]

                try:
                    button_ctx: ComponentContext = await wait_for_component(bot, components=action_row, timeout=15,
                                                                            check=check)  # 10 seconds to reply
                    if button_ctx.component_id == "Yes":
                        if configData["Require Auth Code For High Security Commands"]:
                            try:
                                buttons = [
                                    create_button(style=ButtonStyle.blurple, label="Console Auth", emoji="🖥️",
                                                  custom_id="Console"),
                                    create_button(style=ButtonStyle.blurple, label="Google Auth", emoji="📱",
                                                  custom_id="Google"),
                                ]
                                action_row = create_actionrow(*buttons)
                                embed = discord.Embed(title="Detected High Security Command Usage",
                                                      description=f'Please choose a verification method.',
                                                      color=0xf63737)
                                await button_ctx.edit_origin(embed=embed, components=[action_row], hidden=True)

                                verified = False

                                def check(ctx: ComponentContext):
                                    return ctx.author == ctx.author and ctx.channel == ctx.channel and ctx.component_id in [
                                        "Console", "Google"]

                                try:
                                    button_ctx: ComponentContext = await wait_for_component(bot, components=action_row,
                                                                                            timeout=60, check=check)
                                    if button_ctx.component_id == "Console":
                                        buttons = [
                                            create_button(style=ButtonStyle.green, label="Console Auth", emoji="🖥️",
                                                          custom_id="Console", disabled=True),
                                            create_button(style=ButtonStyle.grey, label="Google Auth", emoji="📱",
                                                          custom_id="Google", disabled=True),
                                        ]
                                        action_row = create_actionrow(*buttons)
                                        embed = discord.Embed(title="Waiting For Verification",
                                                              description=f'Please enter the auth key printed in console.',
                                                              color=0xf63737)
                                        await button_ctx.edit_origin(embed=embed, components=[action_row], hidden=True)
                                        authcode = uuid.uuid4()
                                        print(f'Your auth code is: {authcode}')

                                        def auth_check(msg):
                                            return msg.author == ctx.author and msg.channel == ctx.channel and \
                                                   msg.content.lower() in str(authcode)

                                        msg = await bot.wait_for("message", check=auth_check,
                                                                 timeout=15)  # 10 seconds to reply
                                        await msg.delete()
                                        if msg.content.lower() == str(authcode):
                                            verified = True
                                        else:
                                            verified = False
                                    elif button_ctx.component_id == "Google":

                                        secret = base64.b32encode(bytearray(f'{ctx.author.id}{ctx.author.name}', 'ascii')).decode('utf-8')
                                        url = f'otpauth://totp/Verify?secret={secret}&issuer={ctx.author.name}%20-%20Weather%20Bot%20Auth'

                                        qr = qrcode.QRCode(
                                            version=1,
                                            error_correction=qrcode.constants.ERROR_CORRECT_L,
                                            box_size=10,
                                            border=4,
                                        )
                                        qr.add_data(url)
                                        qr.make(fit=True)
                                        img = qr.make_image(fill_color="white", back_color=(47, 49, 54))
                                        img.save("QR.png")

                                        buttons = [
                                            create_button(style=ButtonStyle.grey, label="Console Auth", emoji="🖥️",
                                                          custom_id="Console", disabled=True),
                                            create_button(style=ButtonStyle.green, label="Google Auth", emoji="📱",
                                                          custom_id="Google", disabled=True),
                                        ]
                                        action_row = create_actionrow(*buttons)
                                        file = discord.File("QR.png")
                                        embed = discord.Embed(title="Waiting For Verification",
                                                              description=f'Please scan the QR code below,\nthen enter the OTP from your phone\n\n**Note**:\n*If you have already scanned you can use old code*',
                                                              color=0xf63737)
                                        embed.set_image(url="attachment://QR.png")
                                        await button_ctx.edit_origin(embed=embed, components=[action_row], hidden=True, file=file)

                                        def googleauth(msg):
                                            totpa = pyotp.TOTP(f'{secret}')
                                            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in str(totpa.now())

                                        msg = await bot.wait_for("message",
                                                                 timeout=30, check=googleauth)  # 30 seconds to reply
                                        await msg.delete()

                                        totp = pyotp.TOTP(f'{secret}')
                                        if msg.content == str(totp.now()):
                                            verified = True
                                        else:
                                            verified = False

                                    if verified:
                                        directory = "./UserData"
                                        files_in_directory = os.listdir(directory)
                                        filtered_files = [file for file in files_in_directory if file.endswith(".json")]
                                        for file in filtered_files:
                                            path_to_file = os.path.join(directory, file)
                                            os.remove(path_to_file)
                                        embed = discord.Embed(title="All User Data Deleted",
                                                              description=f'deleted data for All Users', color=0xf63737)
                                        await ctx.send(embed=embed, hidden=True)
                                        if os.path.exists("QR.png"):
                                            os.remove("QR.png")
                                    else:
                                        embed = discord.Embed(title="Command Canceled",
                                                              description=f'Failed to verify',
                                                              color=0xf63737)
                                        await ctx.send(embed=embed, hidden=True)

                                except asyncio.TimeoutError:
                                    embed = discord.Embed(title="Deletion canceled",
                                                          description=f'You didn''t reply in time!', color=0xf63737)
                                    await ctx.send(embed=embed, components=[], hidden=True)

                            except asyncio.TimeoutError:
                                embed = discord.Embed(title="Deletion canceled",
                                                      description=f'You didn''t reply in time!', color=0xf63737)
                                await ctx.send(embed=embed, components=[], hidden=True)
                        else:
                            directory = "./UserData"
                            files_in_directory = os.listdir(directory)
                            filtered_files = [file for file in files_in_directory if file.endswith(".json")]
                            for file in filtered_files:
                                path_to_file = os.path.join(directory, file)
                                os.remove(path_to_file)
                            embed = discord.Embed(title="All User Data Deleted",
                                                  description=f'deleted data for All Users', color=0xf63737)
                            await ctx.send(embed=embed, components=[], hidden=True)

                    elif button_ctx.component_id == "No":
                        embed = discord.Embed(title="Deletion canceled",
                                              description=f'canceled deletion for all users', color=0xf63737)
                        await ctx.send(embed=embed, components=[], hidden=True)
                    else:
                        embed = discord.Embed(title="Deletion canceled",
                                              description=f'You provided an invalid response', color=0xf63737)
                        await ctx.send(embed=embed, components=[], hidden=True)
                except asyncio.TimeoutError:

                    embed = discord.Embed(title="Deletion canceled",
                                          description=f'You didn''t reply in time!', color=0xf63737)
                    await ctx.send(embed=embed, components=[], hidden=True)
            elif user.startswith("<@"):
                user = user.replace("<", "")
                user = user.replace(">", "")
                user = user.replace("@", "")
                user = user.replace("!", "")
                file = "./UserData/{0}.json".format(str(user))
                try:
                    os.remove(file)
                    embed = discord.Embed(title="Users Data Deleted",
                                          description=f'deleted data for <@{user}>', color=0xf63737)
                    await ctx.send(embed=embed, components=[], hidden=True)
                except FileNotFoundError:
                    embed = discord.Embed(title="User Does Not Exist",
                                          description=f'User ID "{user}" does not have any data stored.',
                                          color=0xf63737)
                    await ctx.send(embed=embed, components=[], hidden=True)
            else:
                embed = discord.Embed(title="<:Error:764493646199521291> | Incorrect Syntax",
                                      description="`/deletedata <user/all>`", color=0xf63737)
                await ctx.send(embed=embed, components=[], hidden=True)

        else:
            embed = discord.Embed(title="<:Error:764493646199521291> | Permission Error",
                                  description="Only bot developers can execute this command", color=0xf63737)
            await ctx.send(embed=embed, components=[], hidden=True)


def setup(bot: Bot):
    bot.add_cog(DeleteData(bot))
