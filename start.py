import os
import discord
from discord_slash import SlashCommand, manage_commands, SlashContext
from discord.ext import commands
import cpuinfo
import psutil
from discord.ext.commands import has_permissions
import koreanbots
import time
from module1 import module1 as md1
import simpleeval
import secrets
import youtube_dl
import ffmpeg

koreanbotstoken = open("koreanbotstoken.txt", "r").read()

Client = commands.Bot(command_prefix="/", intents=discord.Intents.all(), help_command=None)
Client1 = koreanbots.Client(Client, koreanbotstoken)
slash = SlashCommand(client=Client, sync_commands=True)

token = open('token.txt').read()
googleapikey = open('googleapikey.txt').read()

devserver = [812339145942237204, 759260634096467969, 635336036465246218]
icecreamhappydiscord = [635336036465246218]

dev = False

@Client.event
async def on_ready():
    if dev is False:
        await manage_commands.remove_all_commands(711236336308322304, token, devserver)
    print("Ready!")

@Client.event
async def on_member_join(member):
    true_member_count = len([m for m in member.guild.members if not m.bot])
    embed = discord.Embed(title="멤버 입장", description=f'{member.name}님이 {member.guild.name}에 입장했어요!', color=0x00a352)
    embed.add_field(name='현재 인원', value=str(true_member_count) + '명')
    embed.set_footer(text=md1.todaycalculate())
    embed.set_thumbnail(url=member.avatar_url)
    print(member.guild.id)
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
    true_member_count = len([m for m in member.guild.members if not m.bot])
    embed = discord.Embed(title="멤버 퇴장", description=f'{member.name}님이 {member.guild.name}에서 퇴장했어요. ㅠㅠ', color=0xff4747)
    embed.add_field(name='현재 인원', value=str(true_member_count) + '명')
    embed.set_footer(text=md1.todaycalculate())
    embed.set_thumbnail(url=member.avatar_url)
    getchannel = md1.serverdata("insaname", member.guild.id, 123, True)
    try:
        channel = await Client.fetch_channel(getchannel["insaname"])
    except (AttributeError, discord.HTTPException, discord.NotFound):
        pass
    else:
        await channel.send(embed=embed)

@Client.event
async def on_message_delete(message):
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
    embed1 = discord.Embed(name="메시지가 변경되었어요!")
    embed1.add_field(name="변경되기 전 메시지의 콘텐츠", value=before.content, inline=False)
    embed1.add_field(name="변경된 후 메시지의 콘텐츠", value=after.content, inline=False)
    embed1.add_field(name="메시지를 변경한 사람", value=f"<@{after.author.id}>", inline=False)
    embed1.set_footer(text=md1.todaycalculate())
    getchannel = md1.serverdata("logid", after.guild.id, 123, True)
    try:
        channel = await Client.fetch_channel(getchannel["logid"])
    except (AttributeError, discord.errors.HTTPException):
        pass
    else:
        await channel.send(embed=embed1)

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
async def _clean(ctx, amount:int):
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
        await message1.edit(content="이름이 맞지 않는 것 같아요!")
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

@slash.slash(name="random", description="랜덤으로 숫자를 굴려주는 명령어")
async def _random(ctx, x:int, y:int):
    await ctx.send(secrets.SystemRandom().randint(x, y))

@slash.slash(name="getwarn", description="주의를 보는 세상 간단한 명령어")
async def _getwarn(ctx, member:discord.Member):
    warndata = md1.warn(memberid=member.id, amount=0, get=True)
    await ctx.send(f"{member.display_name}님의 주의 개수는 {warndata['warn']}개에요!")

@has_permissions(administrator=True)
@slash.slash(name="warn", description="주의를 주는 세상 복잡한 명령어")
async def _warn(ctx, member:discord.Member, amount:int, reason=None):
    warndata = md1.warn(memberid=member.id, amount=0, get=True)
    warndata = md1.warn(memberid=member.id, amount=warndata['warn'] + amount, get=False)
    if reason is None:
        await ctx.send(f"<@{member.id}>님은 <@{ctx.author.id}>에 의해서 주의를 받았어요! 현재 주의 개수는 {warndata['warn']}개에요!")
    elif reason is not None:
        await ctx.send(f"<@{member.id}>님은 {reason}이라는 이유로 <@{ctx.author.id}>에 의해서 주의를 받았어요! 현재 주의 개수는 {warndata['warn']}개에요!")

@has_permissions(administrator=True)
@slash.slash(name="unwarn", description="주의를 빼는 세상 이상한 명령어")
async def _unwarn(ctx, member:discord.Member, amount:int, reason=None):
    warndata = md1.warn(memberid=member.id, amount=0, get=True)
    warndata = md1.warn(memberid=member.id, amount=warndata['warn'] - amount, get=False)
    if reason is None:
        await ctx.send(f"<@{member.id}>님은 <@{ctx.author.id}>에 의해서 주의가 없어졌어요! 현재 주의 개수는 {warndata['warn']}개에요!")
    elif reason is not None:
        await ctx.send(f"<@{member.id}>님은 {reason}이라는 이유로 <@{ctx.author.id}>에 의해서 주의가 없어졌어요! 현재 주의 개수는 {warndata['warn']}개에요!")

@has_permissions(administrator=True)
@slash.slash(name="hellochannel", description="인사 채널을 설정하는 명령어")
async def _hellochannel(ctx, channel:discord.TextChannel):
    md1.serverdata("insaname", ctx.author.guild.id, channel.id, False)
    await ctx.send(f"{channel.mention}으로 인사 채널이 변경되었어요!")

@slash.slash(name="helpingme", description="제작자가 직접 주는 호감도 확인용")
async def _helpinghands(ctx):
    helpingyouandme = md1.helpingyou(ctx.author.id)
    if helpingyouandme is None:
        await ctx.send("그 사람은 데이터가 없어요!")
    else:
        helpingrank = None
        if ctx.author.id == 338902243476635650:
            helpingrank = "나를 만들어 준 너"
        elif helpingyouandme == 0:
            helpingrank = "이용을 해주는 너"
        elif 0 < helpingyouandme < 100:
            helpingrank = "조금이라도 도와주는 너"
        if helpingrank is None:
            await ctx.send("오류가 난 것 같아요!")
        else:
            embedhelping = discord.Embed(title="호감도 현황", description=f"{ctx.author.name}님! 고마워요!")
            embedhelping.set_author(name="Misile#2134", url="https://github.com/MisileLab", icon_url="https://i.imgur.com/6y4X4aw.png")
            embedhelping.add_field(name="호감도 칭호", value=helpingrank)
            await ctx.send(embed=embedhelping)

@slash.slash(name="noticeother", description="공지를 하는 명령어")
async def _notice(ctx, description:str):
    author = ctx.author
    if author.id != 338902243476635650:
        await ctx.send("이 명령어는 당신이 쓸 수 없어요!")
    elif author.id == 338902243476635650:
        embednotice = discord.Embed(title="공지", description=description, color=0xed2f09)
        embednotice.set_footer(text="by MisileLab", icon_url=ctx.author.avatar_url)
        getchannel = md1.noticeusingbot(ctx.author.guild.id, 0, True)
        message = await ctx.send("공지를 전달 중...")
        for i1 in getchannel:
            try:
                channel = await Client.fetch_channel(i1["gongjiid"])
                await channel.send(embed=embednotice)
            except (AttributeError, discord.NotFound):
                pass
        await message.edit(content="공지를 성공적으로 전달했어요!")

@has_permissions(manage_messages=True, manage_channels=True)
@slash.slash(name="setnotice", description="봇 공지 채널을 정하는 명령어")
async def _setnotice(ctx, channel:discord.TextChannel):
    md1.noticeusingbot(ctx.author.guild.id, channel.id, False)
    await ctx.send(f"{channel.mention}으로 공지 채널이 변경되었어요!")

@slash.slash(name="mining", description="How to 얻는다")
async def _mining(ctx):
    md1.miningmoney(ctx.author.id)
    random1 = secrets.SystemRandom().randint(1, 20)
    if random1 != 1:
        await ctx.send(f"<@{ctx.author.id}>님에게 돈을 줬어요.")
    elif random1 == 1:
        await ctx.send(f"<@{ctx.author.id}>님에게 돈을 줬어요. ㅠㅠ")

@slash.slash(name='getmoney', description='자신의 돈을 확인하는 명령어')
async def _getmoney(ctx):
    getmoney = md1.getmoney(ctx.author.id)
    await ctx.send(f"<@{ctx.author.id}>님의 돈 : {getmoney['level1']}원")

@slash.slash(name='dobak', description="도박하는 명령어, 확률은 50%, 메이플이 아님")
async def _dobak(ctx, money:int):
    try:
        md1.dobakmoney(ctx.author.id, money)
    except md1.FailedDobak:
        await ctx.send(f"<@{ctx.author.id}>님이 도박에서 실패했어요. ㅠㅠ")
    except md1.DontHaveMoney:
        await ctx.send(f"<@{ctx.author.id}>님의 돈이 부족해요!")
    else:
        await ctx.send(f"<@{ctx.author.id}>님이 도박에 성공했어요!")

@slash.slash(name="getcoin", description="무슨 코인을 팔고 있는?")
async def _getcoin(ctx):
    await ctx.send("DM으로 주면 됨 팔고 있는 코인 : 0.00001 [MisileCoin](https://kovan.etherscan.io/token/0x285797e3848d6f5b88c704d8a45c73b2aefbf4d8?a=0x2d1a71b134fbbc3033cf080cf3e4e45dd0dbf485) = 9천만원")

@slash.slash(name="log", description="로그 채널을 지정하는 재밌는 명령어")
async def _log(ctx, channel:discord.TextChannel):
    md1.serverdata('logid', ctx.author.guild.id, channel.id, False)
    await ctx.send(f"로그 채널이 {channel.mention}으로 지정되었어요!")

@slash.slash(name="serverinfo", description="서버 정보를 알려주는 명령어")
async def _serverinfo(ctx, guildid=None):
    message: discord.Message = await ctx.send("서버의 정보를 찾고 있어요!")
    if guildid is None:
        guildid = ctx.author.guild.id
    try:
        guildid = int(guildid)
        guild: discord.Guild = Client.get_guild(guildid)
        if guild is None:
            raise AttributeError
    except (AttributeError, discord.errors.HTTPException, ValueError):
        await message.edit(content="그 서버는 잘못된 서버거나 제가 참여하지 않은 서버인 것 같아요!")
    else:
        embed1 = discord.Embed(name="서버의 정보", description=f"{guild.name}의 정보에요!")
        embed1.add_field(name="길드의 부스트 티어", value=guild.premium_tier)
        embed1.add_field(name="길드의 부스트 개수", value=f"{guild.premium_subscription_count}개")
        embed1.add_field(name="길드 멤버 수(봇 포함)", value=f"{len(guild.members)}명")
        embed1.add_field(name="실제 길드 멤버 수", value=f"{len([m for m in guild.members if not m.bot])}명")
        embed1.set_thumbnail(url=guild.icon_url)
        embed1.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed1.set_footer(text=md1.todaycalculate())
        await message.edit(embed=embed1, content=None)

@slash.slash(name="userinfo", description="유저의 정보를 알려주는 명령어")
async def _userinfo(ctx, userid=None):
    message: discord.Message = await ctx.send("유저를 찾는 중이에요!")
    if userid is None:
        userid = ctx.author.id
    try:
        user1: discord.User = Client.get_user(int(userid))
        if user1 is None:
            raise AttributeError
    except (AttributeError, discord.errors.HTTPException, ValueError):
        await message.edit(content="그 서버는 잘못된 유저거나 제가 알 수 없는 유저인 것 같아요!")
    else:
        embed1 = discord.Embed(name="유저의 정보", description=f"{user1.name}의 정보에요!")
        embed1.set_thumbnail(url=user1.avatar_url)
        embed1.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed1.set_footer(text=md1.todaycalculate())
        embed1.add_field(name="봇 여부", value=str(user1.bot))
        embed1.add_field(name="시스템 계정 여부", value=str(user1.system))
        embed1.add_field(name="계정이 생성된 날짜", value=str(md1.makeformat(user1.created_at)))
        await message.edit(content=None, embed=embed1)

@slash.slash(name="play", description="음악을 틀어주는 명령어", guild_ids=devserver)
async def _play(ctx: SlashContext, music:str):
    correct = False
    message = await ctx.send("잠시만 기다려주세요!")
    if ctx.author.voice is None:
        await message.edit(content="음성 채널에 들어가주세요!")
    else:
        await message.edit(content="지금 음악을 틀기 위한 준비를 하고 있어요!")
        voicechannel: discord.VoiceChannel = ctx.author.voice.channel
        voiceclient: discord.VoiceClient = await voicechannel.connect()
        print("0")
        print(correct)
        if os.path.isfile(f"song{ctx.author.id}.mp3") is True:
            try:
                os.remove(f"song{ctx.author.id}.mp3")
                print("test")
            except PermissionError:
                await message.edit(content="음악을 틀고 있는 것 같아요!")
            else:
                correct = True
        else:
            correct = True
        if correct is True:
            print("1")
            ydl_option = {
                "format": "bestaudio/best",
                "postprocessor": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "aac",
                    "preferredquailty": "192"
                }]
            }
            with youtube_dl.YoutubeDL(ydl_option) as ydl:
                correct = False
                try:
                    ydl.download([music])
                except (youtube_dl.utils.UnavailableVideoError, youtube_dl.utils.DownloadError):
                    result = md1.youtubedownloadmusic(music)
                    print(result)
                    if result is None:
                        await message.edit(content="그런 음악이 없는 것 같아요!")
                    else:
                        print([f'https://youtube.com/watch?v={result}'])
                        try:
                            ydl.download([f"https://youtube.com/watch?v={result}"])
                        except (youtube_dl.utils.UnavailableVideoError, AttributeError, youtube_dl.DownloadError) as e:
                            print(e)
                            await message.edit(content="에러가 난거 같아요!")
                        else:
                            correct = True
                            print("2")
                else:
                    correct = True
                    print("3")
                if correct is True:
                    for file in os.listdir("./"):
                        if file.endswith('.webm'):
                            os.rename(file, f'song{ctx.author.id}.webm')
                            break
                    for file in os.listdir("./"):
                        if file.endswith('.m4a'):
                            os.rename(file, f'song{ctx.author.id}.m4a')
                            break
                    try:
                        stream = ffmpeg.input(f'song{ctx.author.id}.webm')
                        stream = ffmpeg.output(stream, f'song{ctx.author.id}.mp3')
                        ffmpeg.run(stream)
                        os.remove(f'song{ctx.author_id}.webm')
                    except ffmpeg._run.Error:
                        stream = ffmpeg.input(f'song{ctx.author.id}.m4a')
                        stream = ffmpeg.output(stream, f'song{ctx.author.id}.mp3')
                        ffmpeg.run(stream)
                        os.remove(f'song{ctx.author_id}.m4a')
                    await message.edit(content="음악을 틀고 있어요!")
                    music1 = discord.FFmpegOpusAudio(source=f'song{ctx.author.id}.mp3')
                    voiceclient.play(source=music1)

Client.run(token)
