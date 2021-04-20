import discord
from discord_slash import SlashCommand
from discord_slash import manage_commands
from discord.ext import commands
import cpuinfo
import psutil
from discord.ext.commands import has_permissions
import koreanbots
import time
from module1 import module1 as md1
import simpleeval

koreanbotstoken = open("koreanbotstoken.txt", "r").read()

Client = commands.Bot(command_prefix="/", intents=discord.Intents.all(), help_command=None)
Client1 = koreanbots.Client(Client, koreanbotstoken)
slash = SlashCommand(client=Client, sync_commands=True)

token = open('token.txt').read()

devserver = [812339145942237204, 759260634096467969, 635336036465246218]
icecreamhappydiscord = [635336036465246218]

dev = True

@Client.event
async def on_ready():
    if dev is False:
        await manage_commands.remove_all_commands(711236336308322304, token, devserver)
    print("Ready!")

@Client.event
async def on_slash_command_error(ctx, error):
    error1 = str(error)
    if error1.find("You are missing") == 1 and error1.find("permission(s) to run this command.") == 1:
        await ctx.send(f"<@{ctx.author.id}>님은 권한이 없는 것 같아요.")
    elif error1.find("we're now rate limited. retrying after") == 1:
        await ctx.send("조금 이따가 다시 해보세요!")
    else:
        print(error)

@Client.event
async def on_member_join(member):
    true_member_count = len([m for m in member.guild.members if not m.bot])
    embed = discord.Embed(title="멤버 입장", description=f'{member.name}이 {member.guild.name}에 입장했어요!', color=0x00a352)
    embed.add_field(name='현재 인원', value=str(true_member_count) + '명')
    embed.set_footer(text=md1.todaycalculate())
    embed.set_thumbnail(url=member.avatar_url)
    if member.guild.id == 635336036465246218:
        welcomechannel = await Client.fetch_channel(749446018856386651)
        await member.add_roles(member.guild.get_role(826962501097881620))
        await welcomechannel.send(embed=embed)
    else:
        try:
            channel = discord.utils.get(member.guild.channels, name="🔎인사")
            if channel is None:
                raise AttributeError
            else:
                await channel.send(embed=embed)
        except AttributeError:
            pass

@Client.event
async def on_member_remove(member):
    true_member_count = len([m for m in member.guild.members if not m.bot])
    embed = discord.Embed(title="멤버 퇴장", description=f'{member.name}이 {member.guild.name}에서 퇴장했어요. ㅠㅠ', color=0xff4747)
    embed.add_field(name='현재 인원', value=str(true_member_count) + '명')
    embed.set_footer(text=md1.todaycalculate())
    embed.set_thumbnail(url=member.avatar_url)
    try:
        channel = discord.utils.get(member.guild.channels, name="🔎인사")
        if channel is None:
            raise AttributeError
        else:
            await channel.send(embed=embed)
    except discord.HTTPException or AttributeError:
        pass

@Client.command(name="hellothisisverification")
async def idontwantdevelopercommandinthiscommand(ctx):
    await ctx.send("Misile#2134")

@slash.slash(name="bot", description="봇의 정보를 알려주는 명령어")
async def _bot(ctx):
    before = time.monotonic()
    message1 = await ctx.send("Ping Test")
    ping = time.monotonic() - before
    cpuinfo1 = cpuinfo.get_cpu_info()
    embed1 = discord.Embed(title="봇 정보", description="펄럭 봇의 엄청난 봇 정보")
    embed1.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed1.add_field(name="파이썬 버전", value=cpuinfo1["python_version"])
    embed1.add_field(name="CPU 이름", value=cpuinfo1["brand_raw"])
    embed1.add_field(name="CPU Hz", value=cpuinfo1["hz_actual_friendly"])
    embed1.add_field(name="램 전체 용량", value=str(round(psutil.virtual_memory().total / (1024 * 1024 * 1024))) + "GB")
    embed1.add_field(name="램 사용 용량", value=str(round(psutil.virtual_memory().used / (1024 * 1024 * 1024))) + "GB")
    embed1.add_field(name="램 용량 퍼센테이지(%)", value=str(psutil.virtual_memory().percent))
    embed1.add_field(name="봇 핑(ms)", value=str(ping))
    embed1.add_field(name="API 핑(ms)", value=str(round(Client.latency * 1000)))
    await message1.edit(content=None, embed=embed1)

@slash.slash(name="kick", description="상대를 서버 밖으로 날리는 명령어")
@has_permissions(kick_members=True)
async def _kick(ctx, kickmember: discord.Member, reason=None):
    try:
        await kickmember.kick(reason=reason)
    except discord.HTTPException:
        await ctx.send("봇이 권한이 없는 것 같아요.")
    else:
        await ctx.send(f"<@{ctx.author.id}>님으로 인하여 <@{kickmember.id}>가 킥 당했습니다.")

@slash.slash(name="ban", description="상대를 서버 밖으로 영원히 날리는 명령어")
@has_permissions(ban_members=True)
async def _ban(ctx, banmember: discord.Member, reason=None):
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
    embed1.add_field(name="Team Hope", value="[링크](https://teamhopekr.tk/discord)")
    await ctx.send(embed=embed1)

@slash.slash(name="specialthanks", description="이걸 도와준 사람들을 위한 명령어")
async def _specialthanks(ctx):
    embed1 = discord.Embed(name="도와준 사람", description="고마워요!")
    embed1.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed1.add_field(name="Misile#2134", value="잘 버텨준 나")
    embed1.add_field(name="You", value="이 봇을 사용해준 너")
    embed1.add_field(name="FurLuck", value="이 봇의 이미지를 쓰게 해준 펄럭")
    embed1.add_field(name="IceCreamHappy", value="기획자")
    await ctx.send(embed=embed1)

@slash.slash(name="mute", description="상대방을 입막습니다! 읍읍")
@has_permissions(manage_messages=True)
async def _mute(ctx, member:discord.Member, reason=None):
    guild = ctx.guild
    role1 = discord.utils.get(guild.roles, name='Muted')
    if role1 is not None:
        await member.add_roles(role1, reason=reason)
        if reason is None:
            await ctx.send(f"<@{ctx.author.id}>님이 <@{member.id}>님을 뮤트하였습니다!")
        else:
            await ctx.send(f"<@{ctx.author.id}님이 {reason}이라는 이유로 <@{member.id}님을 뮤트하였습니다!")
    else:
        perms1 = discord.Permissions(add_reactions=False, create_instant_invite=False, send_messages=False, speak=False)
        role1 = await guild.create_role(name="Muted", permissions=perms1)
        await member.add_roles(role1, reason=reason)
        if reason is None:
            await ctx.send(f"<@{ctx.author.id}>님이 <@{member.id}>님을 뮤트하였습니다!")
        else:
            await ctx.send(f"<@{ctx.author.id}님이 {reason}이라는 이유로 <@{member.id}님을 뮤트하였습니다!")

@slash.slash(name="unmute", description="상대방을 입 막지 않습니다. 뮤트 멈춰!")
@has_permissions(manage_messages=True)
async def _unmute(ctx, member:discord.Member, reason=None):
    guild = ctx.guild
    role1 = discord.utils.get(guild.roles, name='Muted')
    await member.remove_roles(role1, reason=reason)
    if reason is None:
        await ctx.send(f"<@{ctx.author.id}>님이 <@{member.id}>님을 언뮤트하였습니다!")
    else:
        await ctx.send(f"<@{ctx.author.id}님이 {reason}이라는 이유로 <@{member.id}님을 언뮤트하였습니다!")

@slash.slash(name="calculate", description="계산을 할 수 있는 명령어")
async def _calculate(ctx, calculate):
    try:
        result = simpleeval.simple_eval(calculate)
    except ValueError:
        await ctx.send(f"<@{ctx.author.id}>님, 계산식이 틀린 것 같습니다")
    else:
        await ctx.send(f"<@{ctx.author.id}>님, 계산 결과가 {result}입니다.")

@slash.slash(name="격리", description="격리하는 명령어", guild_ids=icecreamhappydiscord)
async def _guckri(ctx, member:discord.Member, reason=None):
    role1 = ctx.guild.get_role(802733890221375498)
    await member.add_roles(role1, reason=reason)
    if reason is None:
        await ctx.send(f"<@{ctx.author.id}>님이 <@{member.id}>님을 격리하였습니다!")
    else:
        await ctx.send(f"<@{ctx.author.id}님이 {reason}이라는 이유로 <@{member.id}님을 격리하였습니다!")

@slash.slash(name="격리해제", description="격리해제하는 명령어", guild_ids=icecreamhappydiscord)
async def _guckridisable(ctx, member:discord.Member, reason=None):
    role1 = ctx.guild.get_role(802733890221375498)
    await member.remove_roles(role1, reason=reason)
    if reason is None:
        await ctx.send(f"<@{ctx.author.id}>님이 <@{member.id}>님을 격리해제 하였습니다!")
    else:
        await ctx.send(f"<@{ctx.author.id}님이 {reason}이라는 이유로 <@{member.id}님을 격리해제 하였습니다!")

@slash.slash(name="weather", description="날씨를 알려주는 명령어")
async def _weather(ctx, position):
    message1 = await ctx.send("기다려주세요.")
    try:
        weatherdata = md1.get_weather(position)
    except ValueError:
        await ctx.send("이름이 맞지 않는 것 같아요!")
    else:
        embed1 = discord.Embed(name="현재 날씨", description=f"{position}의 날씨에요!")
        embed1.set_thumbnail(url=weatherdata['weatherurl'])
        embed1.add_field(name="현재 온도", value=weatherdata['temp'])
        embed1.add_field(name="최고 온도", value=weatherdata['maxtemp'])
        embed1.add_field(name="최저 온도", value=weatherdata['mintemp'])
        embed1.add_field(name="체감 온도", value=weatherdata['sensibletemp'])
        embed1.add_field(name="날씨 상황", value=weatherdata['cast'])
        embed1.add_field(name="미세먼지 농도(μg/m3)", value=weatherdata['dust'])
        embed1.add_field(name="미세먼지 위험 단계", value=weatherdata['dust_txt'])
        embed1.add_field(name="초미세먼지 농도(μg/m3)", value=weatherdata['ultra_dust'])
        embed1.add_field(name="초미세먼지 위험 단계", value=weatherdata['ultra_dust_txt'])
        embed1.add_field(name="오존 농도(ppm)", value=weatherdata['ozone'])
        embed1.add_field(name="오존 위험 단계", value=weatherdata['ozonetext'])
        await message1.edit(content="완료되었습니다!",embed=embed1)

@slash.slash(name="bitly", description="링크를 길지 않게 만들어주는 명령어")
async def _bitly(ctx, longurl):
    shorturl = md1.shortlink([longurl])
    shorturl2 = str(shorturl).replace("['", "").replace("']", "")
    await ctx.send(f"<@{ctx.author.id}>님 링크가 {shorturl2} 로 변한것 같아요!")

Client.run(token)
