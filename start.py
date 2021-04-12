import discord
from discord_slash import SlashCommand
from discord.ext import commands
import cpuinfo
import psutil
import module1.module1 as md1
from discord.ext.commands import has_permissions, errors
import time
# import koreanbots

client = discord.Client()
koreanbotstoken = open("koreanbotstoken.txt", "r").read()
# Bot = koreanbots.Client(client, koreanbotstoken)

Client = commands.Bot(command_prefix="/", intents=discord.Intents.all())
slash = SlashCommand(client=Client, sync_commands=True)

token = open('token.txt').read()

devserver = [812339145942237204, 759260634096467969]

@Client.command(name="hellothisisverification")
async def idontwantdevelopercommandinthiscommand(ctx):
    await ctx.send("Misile#2134")

@slash.slash(name="bot", description="봇의 정보를 알려주는 명령어")
async def _bot(ctx):
    cpuinfo1 = cpuinfo.get_cpu_info()
    embed1 = discord.Embed(title="봇 정보", description="펄럭 봇의 엄청난 봇 정보")
    embed1.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed1.add_field(name="파이썬 버전", value=cpuinfo1["python_version"])
    embed1.add_field(name="CPU 이름", value=cpuinfo1["brand_raw"])
    embed1.add_field(name="CPU Hz", value=cpuinfo1["hz_actual_friendly"])
    embed1.add_field(name="램 전체 용량", value=str(round(psutil.virtual_memory().total / (1024 * 1024 * 1024))) + "GB")
    embed1.add_field(name="램 사용 용량", value=str(round(psutil.virtual_memory().used / (1024 * 1024 * 1024))) + "GB")
    embed1.add_field(name="램 남은 용량", value=str(round(psutil.virtual_memory().free / (1024 * 1024 * 1024))) + "GB")
    embed1.add_field(name="램 용량 퍼센테이지(%)", value=str(psutil.virtual_memory().percent))
    list1 = md1.getping()
    embed1.add_field(name="숫자 10000개 출력 속도(ms)", value=list1)
    embed1.add_field(name="API 핑(ms)", value=str(round(Client.latency * 1000)))
    await ctx.send(embed=embed1)

@slash.slash(name="kick", description="상대를 서버 밖으로 날리는 명령어")
@has_permissions(kick_members=True)
async def _kick(ctx, kickmember: discord.Member, reason=None):
    errorhandling = await slash.on_slash_command_error(ctx, Exception(errors.MissingPermissions))
    if errorhandling is not None:
        await ctx.send(f"<@{ctx.author.id}>님의 권한이 없습니다.")
    elif errorhandling is None:
        try:
            await kickmember.kick(reason=reason)
        except discord.HTTPException:
            await ctx.send("봇이 권한이 없는 것 같아요.")
        else:
            await ctx.send(f"<@{ctx.author.id}>님으로 인하여 <@{kickmember.id}>가 킥 당했습니다.")

@slash.slash(name="ban", description="상대를 서버 밖으로 영원히 날리는 명령어")
@has_permissions(ban_members=True)
async def _ban(ctx, banmember: discord.Member, reason=None):
    errorhandling = await slash.on_slash_command_error(ctx, Exception(errors.MissingPermissions))
    if errorhandling is not None:
        await ctx.send(f"<@{ctx.author.id}>님의 권한이 없습니다.")
    elif errorhandling is None:
        try:
            await banmember.ban()
        except discord.HTTPException:
            await ctx.send("봇이 권한이 없는 것 같아요.")
        else:
            await ctx.send(f"<@{ctx.author.id}>님으로 인하여 <@{banmember.id}>가 밴되었습니다.")
            dm = await banmember.create_dm()
            if reason is not None:
                await dm.send(f"{reason}으로 인해 밴되었습니다. - by {ctx.author.name}")
            else:
                await dm.send(f"밴되었습니다. - by {ctx.author.name}")

@slash.slash(name="clean", description="채팅청소하는 엄청난 명령어")
@has_permissions(manage_messages=True)
async def _clean(ctx, amount):
    errorhandling = await slash.on_slash_command_error(ctx, Exception(errors.MissingPermissions))
    if errorhandling is not None:
        await ctx.send(f"<@{ctx.author.id}>님은 권한이 없어요!")
    elif errorhandling is None:
        channel1 = ctx.channel
        try:
            await channel1.purge(limit=int(amount))
        except discord.HTTPException:
            await ctx.send("봇이 권한이 없는 것 같아요.")
        else:
            message1 = await ctx.send(f"<@{ctx.author.id}>님이 {str(amount)}만큼 채팅청소 했어요!")
            time.sleep(3)
            await message1.delete()

@slash.slash(name="feedback", description="피드백을 줄 수 있는 명령어")
async def _feedback(ctx):
    embed1 = discord.Embed(name="이 봇의 시스템 정보들", description="여러가지 링크들")
    embed1.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed1.add_field(name="Github", value="[링크](https://github.com/MisileLab/furluck-bot)")
    await ctx.send(embed=embed1)

@slash.slash(name="specialthanks", description="이걸 도와준 사람들을 위한 명령어")
async def _specialthanks(ctx):
    embed1 = discord.Embed(name="도와준 사람", description="고마워요!")
    embed1.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed1.add_field(name="Misile#2134", value="잘 버텨준 나")
    embed1.add_field(name="You", value="이 봇을 사용해준 너")
    embed1.add_field(name="FurLuck", value="이 봇의 이미지를 쓰게 해준 펄럭")
    await ctx.send(embed=embed1)


Client.run(token)
