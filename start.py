import os
import discord
from discord.ext import commands
from discord.ext.commands.errors import ExtensionAlreadyLoaded
import koreanbots
from cogs.modules import module1 as md1
from cogs.modules import module2 as md2
from dislash import slash_commands
from dotenv import dotenv_values

dotenvvalues = dotenv_values(".env")
koreanbotstoken = dotenvvalues["koreanbotstoken"]
token = dotenvvalues["token"]

Client = commands.Bot(command_prefix="/", intents=discord.Intents.all(), help_command=None)
Client1 = koreanbots.Koreanbots(Client, koreanbotstoken)
slash = slash_commands.SlashClient(Client)

icecreamhappydiscord = [635336036465246218]
ignore_error = commands.CommandNotFound, discord.errors.NotFound
message_error = slash_commands.MissingPermissions, slash_commands.BotMissingPermissions, \
                slash_commands.CommandOnCooldown


for file in os.listdir("cogs"):
    if file.endswith(".py"):
        Client.load_extension(f"cogs.{file[:-3]}")
        print(f"cogs.{file[:-3]} - 로드 성공!")


@slash.event
async def on_ready():
    print("Slash Client Ready!")


# noinspection PyUnusedLocal
@Client.event
async def on_command_error(error):
    if not isinstance(error, ignore_error):
        raise error


@slash.event
async def on_slash_command_error(inter, error):
    if not isinstance(error, ignore_error):
        if isinstance(error, message_error):
            await md2.sub_error_handler(error, inter)
        else:
            raise error


@Client.event
async def on_member_join(member):
    embed = md2.make_embed(member)
    getchannel = md1.serverdata("insaname", member.guild.id, 123, True)
    try:
        channel = await Client.fetch_channel(getchannel["insaname"])
    except (AttributeError, discord.HTTPException, discord.NotFound):
        pass
    else:
        await channel.send(embed=embed)
        if member.guild.id == 635336036465246218:
            await member.add_roles(member.guild.get_role(826962501097881620))


@Client.event
async def on_member_remove(member):
    embed = md2.make_member_remove_embed(member)
    getchannel = md1.serverdata("insaname", member.guild.id, 123, True)
    try:
        channel = await Client.fetch_channel(getchannel["insaname"])
    except (AttributeError, discord.HTTPException, discord.NotFound):
        pass
    else:
        await channel.send(embed=embed)


@Client.event
async def on_message_delete(message):
    if message.author.bot is False:
        embed1 = discord.Embed(name="메시지가 삭제되었어요!")
        embed1.add_field(name="삭제된 메시지의 내용", value=message.content, inline=False)
        embed1.add_field(name="삭제된 메시지를 보낸 사람", value=f"<@{message.author.id}>", inline=False)
        embed1.add_field(name="삭제된 메시지가 보내진 채널", value=message.channel.mention, inline=False)
        embed1.set_footer(text=md1.todaycalculate())
        getchannel = md1.serverdata("logid", message.guild.id, 123, True)
        try:
            channel = await Client.fetch_channel(getchannel["logid"])
        except (AttributeError, discord.HTTPException, discord.NotFound):
            pass
        else:
            await channel.send(embed=embed1)


@Client.event
async def on_message_edit(before, after):
    if after.author.bot is True:
        return
    try:
        after.attachments[0].url
    except IndexError:
        pass
    else:
        if after.attachments[0].url is not None:
            embed1 = md1.get_message_edit_embed(before, after)
            getchannel = md1.serverdata("logid", after.guild.id, 123, True)
            try:
                channel = await Client.fetch_channel(getchannel["logid"])
            except (AttributeError, discord.errors.HTTPException):
                pass
            else:
                await channel.send(embed=embed1)


@Client.command(name="hellothisisverification")
async def oneforgottendiscordslashcommandkoreanbotlistnoslashcommandlol(ctx):
    await ctx.send("Misile#1231")

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        try:
            Client.load_extension(f"cogs.{file[:-3]}")
        except ExtensionAlreadyLoaded:
            break
        print(f"cogs.{file[:-3]} Loaded")

Client.run(token)
