import discord
from discord.ext import commands
import cpuinfo
import psutil
import koreanbots
import time
from module1 import module1 as md1
import simpleeval
import secrets
from dislash import slash_commands, Type, Button, ActionRow, ButtonStyle
from dislash.interactions import Interaction
from module1 import module2 as md2

koreanbotstoken = open("koreanbotstoken.txt", "r").read()
token = open('token.txt').read()
googleapikey = open('googleapikey.txt').read()

Client = commands.Bot(command_prefix="/", intents=discord.Intents.all(), help_command=None)
Client1 = koreanbots.Client(Client, koreanbotstoken)
slash = slash_commands.SlashClient(Client)

devserver = [812339145942237204, 759260634096467969, 635336036465246218]
icecreamhappydiscord = [635336036465246218]

@Client.event
async def on_ready():
    print("Ready!")

@slash.event
async def on_ready():
    print("Slash Client Ready!")

@slash.event
async def on_slash_command_error(inter, error):
    ignore_error = commands.CommandNotFound
    if isinstance(error, ignore_error):
        pass

    if isinstance(error, slash_commands.MissingPermissions):
        await inter.reply(f"권한이 부족해요! 부족한 권한 : {error.missing_perms}")

    if isinstance(error, slash_commands.BotMissingPermissions):
        await inter.reply(f"봇의 권한이 부족해요! 부족한 권한 : {error.missing_perms}")

    if isinstance(error, slash_commands.CommandOnCooldown):
        await inter.reply(f"아직 이 명령어는 {error.cooldown}초 뒤에 사용할 수 있어요!")

@Client.event
async def on_member_join(member):
    true_member_count = len([m for m in member.guild.members if not m.bot])
    embed = discord.Embed(title="멤버 입장", description=f'{member.name}님이 {member.guild.name}에 입장했어요!', color=0x00a352)
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
    if after.author.bot is False:
        try:
            after.attachments[0].url
        except IndexError:
            pass
        else:
            if after.attachments[0].url is not None:
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

@slash.command(name="bot", description="봇의 정보를 알려주는 명령어")
async def _bot(inter: Interaction):
    before = time.monotonic()
    await inter.reply("Ping Test")
    ping = time.monotonic() - before
    cpuinfo1 = cpuinfo.get_cpu_info()
    embed1 = discord.Embed(title="봇 정보", description="펄럭 봇의 엄청난 봇 정보")
    embed1.set_author(name=inter.author.name, icon_url=inter.author.avatar_url)
    embed1.add_field(name="파이썬 버전", value=cpuinfo1["python_version"])
    embed1.add_field(name="CPU 이름", value=cpuinfo1["brand_raw"])
    embed1.add_field(name="CPU Hz", value=cpuinfo1["hz_actual_friendly"])
    embed1.add_field(name="램 전체 용량", value=str(round(psutil.virtual_memory().total / (1024 * 1024 * 1024))) + "GB")
    embed1.add_field(name="램 사용 용량", value=str(round(psutil.virtual_memory().used / (1024 * 1024 * 1024))) + "GB")
    embed1.add_field(name="램 용량 퍼센테이지(%)", value=str(psutil.virtual_memory().percent))
    embed1.add_field(name="봇 핑(ms)", value=str(ping))
    embed1.add_field(name="API 핑(ms)", value=str(round(Client.latency * 1000)))
    await inter.edit(content=None, embed=embed1)

kickoption = md2.NewOptionList()
kickoption.make_option(name="member", description="킥할 사람", required=True, type=Type.USER)
kickoption.make_option(name="reason", description="왜 킥함?", required=False, type=Type.STRING)
@slash.command(name="kick", description="상대를 서버 밖으로 날리는 명령어", options=kickoption)
@slash_commands.has_guild_permissions(kick_members=True)
# @slash_commands.bot_has_guild_permissions(kick_members=True)
async def _kick(inter:Interaction):
    kickmember = inter.get('member')
    reason = inter.get('reason', None)
    await kickmember.kick(reason=reason)
    await inter.reply(f"<@{inter.author.id}>님으로 인하여 <@{kickmember.id}>가 킥 당했습니다.")

banoption = md2.NewOptionList()
banoption.make_option(name="member", description="밴할 멤버", required=True, type=Type.USER)
banoption.make_option(name="reason", description="왜 밴함", required=False, type=Type.STRING)
@slash.command(name="ban", description="상대를 서버 밖으로 영원히 날리는 명령어", options=banoption)
@slash_commands.has_guild_permissions(ban_members=True)
# @slash_commands.bot_has_guild_permissions(ban_members=True)
async def _ban(inter:Interaction):
    banmember: discord.Member = inter.get('member')
    reason = inter.get('reason', None)
    await banmember.ban()
    await inter.reply(f"<@{inter.author.id}>님으로 인하여 <@{banmember.id}>가 밴되었습니다.")
    dm = await banmember.create_dm()
    if reason is not None: 
        await dm.send(f"{reason}으로 인해 밴되었습니다. - by {inter.author.name}")
    else:
        await dm.send(f"밴되었습니다. - by {inter.author.name}")

cleanoption = md2.NewOptionList()
cleanoption.make_option(name="amount", description="채팅청소하는 수", required=False, type=Type.INTEGER)
@slash.command(name="clean", description="채팅청소하는 엄청난 명령어", options=cleanoption)
@slash_commands.has_guild_permissions(manage_messages=True)
# @slash_commands.bot_has_guild_permissions(manage_messages=True)
async def _clean(inter:Interaction):
    amount: int = inter.get('amount')
    channel1 = inter.channel
    await channel1.purge(limit=int(amount))
    await inter.reply(f"<@{inter.author.id}>님이 {str(amount)}만큼 채팅청소 했어요!")
    time.sleep(3)
    await inter.delete()

@slash.command(name="feedback", description="피드백을 줄 수 있는 명령어")
async def _feedback(inter:Interaction):
    embed1 = discord.Embed(name="이 봇의 시스템 정보들", description="여러가지 링크들")
    embed1.set_author(name=inter.author.name, icon_url=inter.author.avatar_url)
    embed1.add_field(name="Github", value="[링크](https://github.com/MisileLab/furluck-bot)")
    await inter.reply(embed=embed1)

@slash.command(name="specialthanks", description="Thank you for helping me")
async def _specialthanks(inter:Interaction):
    row = ActionRow(Button(
        style=ButtonStyle.green,
        label="Click Please",
        custom_id="buttonhelping"
    ))
    embed1 = discord.Embed(name="Helping hands", description="Thank you")
    embed1.set_author(name=inter.author.name, icon_url=inter.author.avatar_url)
    embed1.add_field(name="Misile#2134", value="Written by me")
    embed1.add_field(name="You", value="Using my bot")
    embed1.add_field(name="FurLuck", value="This bot image author")
    msg = await inter.reply(embed=embed1, components=[row])
    await msg.wait_for_button_click()
    embed2 = discord.Embed(name="Helping hands", description="Thank you")
    embed2.add_field(name="EQUENOS", value="Github Pull request #1, dislash.py developer")
    await inter.edit(embed=embed2)


muteoption = md2.NewOptionList()
muteoption.make_option(name="member", description="뮤트할 사람", required=True, type=Type.USER)
muteoption.make_option(name="reason", description="왜 뮤트함?", required=False, type=Type.STRING)
@slash.command(name="mute", description="상대방을 입막습니다! 읍읍", options=muteoption)
@slash_commands.has_guild_permissions(manage_messages=True)
# @slash_commands.bot_has_guild_permissions(manage_messages=True)
async def _mute(inter:Interaction):
    member: discord.Member = inter.get('member')
    reason = inter.get('reason', None)
    guild = inter.guild
    role1 = discord.utils.get(guild.roles, name='Muted')
    if role1 is not None:
        await member.add_roles(role1, reason=reason)
        if reason is None:
            await inter.reply(f"<@{inter.author.id}>님이 <@{member.id}>님을 뮤트하였습니다!")
        else:
            await inter.reply(f"<@{inter.author.id}님이 {reason}이라는 이유로 <@{member.id}님을 뮤트하였습니다!")
    else:
        perms1 = discord.Permissions(add_reactions=False, create_instant_invite=False, send_messages=False, speak=False)
        role1 = await guild.create_role(name="Muted", permissions=perms1)
        await member.add_roles(role1, reason=reason)
        if reason is None:
            await inter.reply(f"<@{inter.author.id}>님이 <@{member.id}>님을 뮤트하였습니다!")
        else:
            await inter.reply(f"<@{inter.author.id}님이 {reason}이라는 이유로 <@{member.id}님을 뮤트하였습니다!")

unmuteoption = md2.NewOptionList()
unmuteoption.make_option(name="member", description="언뮤트할 사람", required=True, type=Type.USER)
unmuteoption.make_option(name="reason", description="왜 언뮤트함?", required=False, type=Type.STRING)
@slash.command(name="unmute", description="상대방을 입 막지 않습니다. 뮤트 멈춰!", options=unmuteoption)
@slash_commands.has_guild_permissions(manage_messages=True)
# @slash_commands.bot_has_guild_permissions(manage_messages=True)
async def _unmute(inter:Interaction):
    member: discord.Member = inter.get('member')
    reason = inter.get('reason', None)
    guild = inter.guild
    role1 = discord.utils.get(guild.roles, name='뮤트')
    await member.remove_roles(role1, reason=reason)
    if reason is None:
        await inter.reply(f"<@{inter.author.id}>님이 <@{member.id}>님을 언뮤트하였습니다!")
    else:
        await inter.reply(f"<@{inter.author.id}님이 {reason}이라는 이유로 <@{member.id}님을 언뮤트하였습니다!")

calculateoption = md2.NewOptionList()
calculateoption.make_option(name="calculate", description="계산할 식", required=True, type=Type.STRING)
@slash.command(name="calculate", description="계산을 할 수 있는 명령어", options=calculateoption)
async def _calculate(inter:Interaction):
    calculate = inter.get('calculate')
    try:
        result = simpleeval.simple_eval(calculate)
    except ValueError:
        await inter.reply(f"<@{inter.author.id}>님, 계산식이 틀린 것 같습니다")
    except ZeroDivisionError:
        await inter.reply("0으로 나누다?")
    else:
        await inter.reply(f"<@{inter.author.id}>님, 계산 결과가 {result}입니다.")

guckrioption = md2.NewOptionList()
guckrioption.make_option(name="member", description="격리할 사람", required=True, type=Type.USER)
guckrioption.make_option(name="reason", description="격리하는 이유", required=False, type=Type.STRING)
@slash.command(name="격리", description="격리하는 명령어", guild_ids=icecreamhappydiscord, options=guckrioption)
@slash_commands.has_guild_permissions(administrator=True)
# @slash_commands.bot_has_guild_permissions(administrator=True)
async def _guckri(inter: Interaction):
    member = inter.get('member')
    reason = inter.get('reason', None)
    role1 = inter.guild.get_role(802733890221375498)
    await member.add_roles(role1, reason=reason)
    if reason is None:
        await inter.reply(f"<@{inter.author.id}>님이 <@{member.id}>님을 격리하였습니다!")
    else:
        await inter.reply(f"<@{inter.author.id}님이 {reason}이라는 이유로 <@{member.id}님을 격리하였습니다!")

guckridisableoption = md2.NewOptionList()
guckridisableoption.make_option(name="member", description="격리 해제할 멤버", required=True, type=Type.USER)
guckridisableoption.make_option(name="reason", description="격리 해제하는 이유", required=False, type=Type.STRING)
@slash.command(name="격리해제", description="격리해제하는 명령어", guild_ids=icecreamhappydiscord, options=guckridisableoption)
@slash_commands.has_guild_permissions(administrator=True)
# @slash_commands.bot_has_guild_permissions(administrator=True)
async def _guckridisable(inter:Interaction):
    member = inter.get('member')
    reason = inter.get('reason', None)
    role1 = inter.guild.get_role(802733890221375498)
    await member.remove_roles(role1, reason=reason)
    if reason is None:
        await inter.reply(f"<@{inter.author.id}>님이 <@{member.id}>님을 격리해제 하였습니다!")
    else:
        await inter.reply(f"<@{inter.author.id}님이 {reason}이라는 이유로 <@{member.id}님을 격리해제 하였습니다!")

weatheroption = md2.NewOptionList()
weatheroption.make_option(name="position", description="날씨를 알고 싶은 장소", required=False, type=Type.STRING)
@slash.command(name="weather", description="날씨를 알려주는 명령어 (네이버 날씨)", options=weatheroption)
async def _weather(inter:Interaction):
    await inter.reply("기다려주세요.")
    position = inter.get('position', None)
    try:
        weatherdata = md1.get_weather(position)
    except ValueError:
        await inter.edit(content="이름이 맞지 않는 것 같아요!")
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
        await inter.edit(content="완료되었습니다!",embed=embed1)

bitlyoption = md2.NewOptionList()
bitlyoption.make_option(name="url", description="길지 않게 만들 링크", required=True, type=Type.STRING)
@slash.command(name="bitly", description="링크를 길지 않게 만들어주는 명령어", options=bitlyoption)
async def _bitly(inter:Interaction):
    longurl = inter.get('url')
    shorturl = md1.shortlink([longurl])
    shorturl2 = str(shorturl).replace("['", "").replace("']", "")
    await inter.reply(f"<@{inter.author.id}>님 링크가 {shorturl2} 로 변한것 같아요!")

randomoption = md2.NewOptionList()
randomoption.make_option(name="min", description="최소 숫자", required=True, type=Type.INTEGER)
randomoption.make_option(name="max", description="최대 숫자", required=True, type=Type.INTEGER)
@slash.command(name="random", description="랜덤으로 숫자를 굴려주는 명령어", options=randomoption)
async def _random(inter:Interaction):
    x = inter.get('min')
    y = inter.get('max')
    await inter.reply(secrets.SystemRandom().randint(x, y))

getwarnoption = md2.NewOptionList()
getwarnoption.make_option(name="member", description="누구의 주의를 볼거임?", type=Type.USER, required=False)
@slash.command(name="getwarn", description="주의를 보는 세상 간단한 명령어", options=getwarnoption)
async def _getwarn(inter:Interaction):
    member: discord.Member = inter.get('member', inter.author.id)
    warndata = md1.warn(memberid=member.id, amount=0, get=True)
    await inter.reply(f"{member.display_name}님의 주의 개수는 {warndata['warn']}개에요!")

warnoption = md2.NewOptionList()
warnoption.make_option(name="member", description="주의를 줄 사람", required=True, type=Type.USER)
warnoption.make_option(name="reason", description="주의를 주는 이유", required=False, type=Type.STRING)
warnoption.make_option(name="amount", description="주의를 얼마나 줄거임?", required=True, type=Type.INTEGER)
@slash_commands.has_guild_permissions(administrator=True)
# @slash_commands.bot_has_guild_permissions(administrator=True)
@slash.command(name="warn", description="주의를 주는 세상 복잡한 명령어", options=warnoption)
async def _warn(inter:Interaction):
    member = inter.get('member')
    reason = inter.get('reason', None)
    amount = inter.get('amount')
    warndata = md1.warn(memberid=member.id, amount=0, get=True)
    warndata = md1.warn(memberid=member.id, amount=warndata['warn'] + amount, get=False)
    if reason is None:
        await inter.reply(f"<@{member.id}>님은 <@{inter.author.id}>에 의해서 주의를 받았어요! 현재 주의 개수는 {warndata['warn']}개에요!")
    elif reason is not None:
        await inter.reply(f"<@{member.id}>님은 {reason}이라는 이유로 <@{inter.author.id}>에 의해서 주의를 받았어요! 현재 주의 개수는 {warndata['warn']}개에요!")

unwarnoption = md2.NewOptionList()
unwarnoption.make_option(name="member", description="주의를 줄 사람", required=True, type=Type.USER)
unwarnoption.make_option(name="reason", description="주의를 주는 이유", required=False, type=Type.STRING)
unwarnoption.make_option(name="amount", description="주의를 얼마나 줄거임?", required=True, type=Type.INTEGER)
@slash_commands.has_guild_permissions(administrator=True)
# @slash_commands.bot_has_guild_permissions(administrator=True)
@slash.command(name="unwarn", description="주의를 빼는 세상 이상한 명령어", options=unwarnoption)
async def _unwarn(inter:Interaction):
    member = inter.get('member')
    reason = inter.get('reason', None)
    amount = inter.get('amount')
    warndata = md1.warn(memberid=member.id, amount=0, get=True)
    warndata = md1.warn(memberid=member.id, amount=warndata['warn'] - amount, get=False)
    if reason is None:
        await inter.reply(f"<@{member.id}>님은 <@{inter.author.id}>에 의해서 주의가 없어졌어요! 현재 주의 개수는 {warndata['warn']}개에요!")
    elif reason is not None:
        await inter.reply(f"<@{member.id}>님은 {reason}이라는 이유로 <@{inter.author.id}>에 의해서 주의가 없어졌어요! 현재 주의 개수는 {warndata['warn']}개에요!")

hellochannel = md2.NewOptionList()
hellochannel.make_option(name="channel", description="인사 채널 (꼭 텍스트 채널이어야 함)", required=True, type=Type.CHANNEL)
@slash_commands.has_guild_permissions(administrator=True)
# @slash_commands.bot_has_guild_permissions(administrator=True)
@slash.command(name="hellochannel", description="인사 채널을 설정하는 명령어", options=hellochannel)
async def _hellochannel(inter:Interaction):
    channel = inter.get("channel")
    if type(channel) is discord.TextChannel:
        md1.serverdata("insaname", inter.author.guild.id, channel.id, False)
        await inter.reply(f"{channel.mention}으로 인사 채널이 변경되었어요!")

userchannel = md2.NewOptionList()
userchannel.make_option(name="user", description="호감도를 확인할 유저", required=False, type=Type.USER)
@slash.command(name="helpingme", description="제작자가 직접 주는 호감도 확인용", options=userchannel)
async def _helpinghands(inter:Interaction):
    user = inter.get("user", None)
    if user is None:
        user: discord.Member = inter.author
    helpingyouandme = md1.helpingyou(user.id)
    if helpingyouandme is None:
        await inter.reply("그 사람은 데이터가 없어요!")
    else:
        helpingrank = None
        if user.id == 338902243476635650:
            helpingrank = "나를 만들어 준 너"
        elif helpingyouandme == 0:
            helpingrank = "이용을 해주는 너"
        elif 0 < helpingyouandme < 100:
            helpingrank = "조금이라도 도와주는 너"
        if helpingrank is None:
            await inter.reply("오류가 난 것 같아요!")
        else:
            embedhelping = discord.Embed(title="호감도 현황", description=f"{user.name}님! 고마워요!")
            embedhelping.set_author(name="Misile#2134", url="https://github.com/MisileLab", icon_url="https://i.imgur.com/6y4X4aw.png")
            embedhelping.add_field(name="호감도 칭호", value=helpingrank)
            await inter.reply(embed=embedhelping)

noticeother = md2.NewOptionList()
noticeother.make_option(name="description", description="설명", required=True, type=Type.STRING)
@slash.command(name="noticeother", description="공지를 하는 명령어", options=noticeother)
async def _notice(inter:Interaction, description:str):
    author = inter.author
    if author.id != 338902243476635650:
        await inter.reply("이 명령어는 당신이 쓸 수 없어요!")
    elif author.id == 338902243476635650:
        embednotice = discord.Embed(title="공지", description=description, color=0xed2f09)
        embednotice.set_footer(text="by MisileLab", icon_url=inter.author.avatar_url)
        getchannel = md1.noticeusingbot(inter.author.guild.id, 0, True)
        await inter.reply("공지를 전달 중...")
        for i1 in getchannel:
            try:
                channel: discord.TextChannel = await Client.fetch_channel(i1["gongjiid"])
                await channel.send(embed=embednotice)
            except (AttributeError, discord.NotFound):
                pass
        await inter.edit(content="공지를 성공적으로 전달했어요!")

setnotice = md2.NewOptionList()
setnotice.make_option(name="channel", description="봇 공지 채널", required=True, type=Type.CHANNEL)
@slash_commands.has_guild_permissions(manage_messages=True, manage_channels=True)
# @slash_commands.bot_has_guild_permissions(manage_messages=True, manage_channels=True)
@slash.command(name="setnotice", description="봇 공지 채널을 정하는 명령어", options=setnotice)
async def _setnotice(inter:Interaction):
    channel = inter.get("setnotice")
    md1.noticeusingbot(inter.author.guild.id, channel.id, False)
    await inter.reply(f"{channel.mention}으로 공지 채널이 변경되었어요!")

@slash_commands.cooldown(10, 600)
@slash.command(name="mining", description="How to 얻는다, 600초 당 10번 씩 가능")
async def _mining(inter:Interaction):
    md1.miningmoney(inter.author.id)
    random1 = secrets.SystemRandom().randint(1, 20)
    if random1 != 1:
        await inter.reply(f"<@{inter.author.id}>님에게 돈을 줬어요.")
    elif random1 == 1:
        await inter.reply(f"<@{inter.author.id}>님에게 돈을 줬어요. ㅠㅠ")

@slash.command(name='getmoney', description='자신의 돈을 확인하는 명령어')
async def _getmoney(inter:Interaction):
    getmoney = md1.getmoney(inter.author.id)
    await inter.reply(f"<@{inter.author.id}>님의 돈 : {getmoney}원")

dobak = md2.NewOptionList()
dobak.make_option(name="money", description="도박할 돈", required=True, type=Type.INTEGER)
@slash.command(name='dobak', description="도박하는 명령어, 확률은 50%, 메이플이 아님", options=dobak)
async def _dobak(inter:Interaction, money:int):
    try:
        md1.dobakmoney(inter.author.id, money)
    except md1.FailedDobak:
        await inter.reply(f"<@{inter.author.id}>님이 도박에서 실패했어요. ㅠㅠ")
    except md1.DontHaveMoney:
        await inter.reply(f"<@{inter.author.id}>님의 돈이 부족해요!")
    else:
        await inter.reply(f"<@{inter.author.id}>님이 도박에 성공했어요!")

@slash.command(name="getcoin", description="무슨 코인을 팔고 있는?")
async def _getcoin(inter:Interaction):
    await inter.reply("DM으로 주면 됨 팔고 있는 코인 : 0.00001 [MisileCoin](https://kovan.etherscan.io/token/0x285797e3848d6f5b88c704d8a45c73b2aefbf4d8?a=0x2d1a71b134fbbc3033cf080cf3e4e45dd0dbf485) = 9천만원")

logoption = md2.NewOptionList()
logoption.make_option(name="channel", description="로그 채널", type=Type.CHANNEL, required=True)
@slash.command(name="log", description="로그 채널을 지정하는 재밌는 명령어")
async def _log(inter:Interaction):
    channel = inter.get("channel")
    md1.serverdata('logid', inter.author.guild.id, channel.id, False)
    await inter.reply(f"로그 채널이 {channel.mention}으로 지정되었어요!")

serverinfo = md2.NewOptionList()
serverinfo.make_option(name="serverid", description="서버 ID", type=Type.INTEGER, required=False)
@slash.command(name="serverinfo", description="서버 정보를 알려주는 명령어")
async def _serverinfo(inter:Interaction):
    await inter.reply("서버의 정보를 찾고 있어요!")
    guildid = inter.get("serverid", None)
    if guildid is None:
        guildid = inter.author.guild.id
    try:
        guildid = int(guildid)
        guild: discord.Guild = Client.get_guild(guildid)
        if guild is None:
            raise AttributeError
    except (AttributeError, discord.errors.HTTPException, ValueError):
        await inter.edit(content="그 서버는 잘못된 서버거나 제가 참여하지 않은 서버인 것 같아요!")
    else:
        embed1 = discord.Embed(name="서버의 정보", description=f"{guild.name}의 정보에요!")
        embed1.add_field(name="길드의 부스트 티어", value=guild.premium_tier)
        embed1.add_field(name="길드의 부스트 개수", value=f"{guild.premium_subscription_count}개")
        embed1.add_field(name="길드 멤버 수(봇 포함)", value=f"{len(guild.members)}명")
        embed1.add_field(name="실제 길드 멤버 수", value=f"{len([m for m in guild.members if not m.bot])}명")
        embed1.set_thumbnail(url=guild.icon_url)
        embed1.set_author(name=inter.author.name, icon_url=inter.author.avatar_url)
        embed1.set_footer(text=md1.todaycalculate())
        await inter.edit(embed=embed1, content=None)

userinfo = md2.NewOptionList()
userinfo.make_option(name="serverid", description="서버 ID", type=Type.INTEGER, required=False)
@slash.command(name="userinfo", description="유저의 정보를 알려주는 명령어", options=userinfo)
async def _userinfo(inter:Interaction):
    userid = inter.get("serverid")
    await inter.reply("유저를 찾는 중이에요!")
    if userid is None:
        userid = inter.author.id
    try:
        user1: discord.User = Client.get_user(int(userid))
        if user1 is None:
            raise AttributeError
    except (AttributeError, discord.errors.HTTPException, ValueError):
        await inter.edit(content="그 서버는 잘못된 유저거나 제가 알 수 없는 유저인 것 같아요!")
    else:
        embed1 = discord.Embed(name="유저의 정보", description=f"{user1.name}의 정보에요!")
        embed1.set_thumbnail(url=user1.avatar_url)
        embed1.set_author(name=inter.author.name, icon_url=inter.author.avatar_url)
        embed1.set_footer(text=md1.todaycalculate())
        embed1.add_field(name="봇 여부", value=str(user1.bot))
        embed1.add_field(name="시스템 계정 여부", value=str(user1.system))
        embed1.add_field(name="계정이 생성된 날짜", value=str(md1.makeformat(user1.created_at)))
        await inter.edit(content=None, embed=embed1)

musicinfo = md2.NewOptionList()
musicinfo.make_option(name="music", description="음악 링크나 검색어", type=Type.STRING, required=True)
@slash.command(name="play", description="음악을 틀어주는 명령어", guild_ids=devserver, options=musicinfo)
async def _play(inter:Interaction):
    music = inter.get("music")
    await md1.playvoiceclient(inter, music, get=True)

Client.run(token)
