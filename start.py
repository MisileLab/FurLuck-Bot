import discord
from discord.ext import commands
import cpuinfo
import koreanbots
import time
from modules import module1 as md1
from modules import module2 as md2
import simpleeval
import secrets
from dislash import slash_commands, Type, Button, ActionRow, ButtonStyle, ClickListener
from dislash.interactions import SlashInteraction

koreanbotstoken = open("koreanbotstoken.txt", "r").read()
token = open('token.txt').read()

Client = commands.Bot(command_prefix="/", intents=discord.Intents.all(), help_command=None)
Client1 = koreanbots.Koreanbots(Client, koreanbotstoken)
slash = slash_commands.SlashClient(Client)

devserver = [812339145942237204, 635336036465246218, 863950154055155712]
icecreamhappydiscord = [635336036465246218]
ignore_error = commands.CommandNotFound, discord.errors.NotFound
message_error = slash_commands.MissingPermissions, slash_commands.BotMissingPermissions, \
                slash_commands.CommandOnCooldown


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


@slash.command(name="bot", description="봇의 정보를 알려주는 명령어")
async def _bot(inter: SlashInteraction):
    before = time.monotonic()
    await inter.reply(type=5)
    ping = time.monotonic() - before
    cpuinfo1 = cpuinfo.get_cpu_info()
    embed1 = md1.make_embed_bot_information(inter, cpuinfo1, ping, Client)
    await inter.edit(content=None, embed=embed1)


kickoption = md1.NewOptionList()
kickoption.make_option(name="member", description="킥할 사람", required=True, type=Type.USER)
kickoption.make_option(name="reason", description="왜 킥함?", required=False, type=Type.STRING)


@slash.command(name="kick", description="상대를 서버 밖으로 날리는 명령어", options=kickoption.options)
@slash_commands.has_guild_permissions(kick_members=True)
@slash_commands.bot_has_guild_permissions(kick_members=True)
async def _kick(inter: SlashInteraction):
    kickmember = inter.get('member')
    reason = inter.get('reason', None)
    await kickmember.kick(reason=reason)
    await inter.reply(f"<@{inter.author.id}>님으로 인하여 <@{kickmember.id}>가 킥 당했습니다.")


banoption = md1.NewOptionList()
banoption.make_option(name="member", description="밴할 멤버", required=True, type=Type.USER)
banoption.make_option(name="reason", description="왜 밴함", required=False, type=Type.STRING)


@slash.command(name="ban", description="상대를 서버 밖으로 영원히 날리는 명령어", options=banoption.options)
@slash_commands.has_guild_permissions(ban_members=True)
@slash_commands.bot_has_guild_permissions(ban_members=True)
async def _ban(inter: SlashInteraction):
    banmember: discord.Member = inter.get('member')
    reason = inter.get('reason', None)
    await banmember.ban()
    await inter.reply(f"<@{inter.author.id}>님으로 인하여 <@{banmember.id}>가 밴되었습니다.")
    dm = await banmember.create_dm()
    if reason is not None:
        await dm.send(f"{reason}으로 인해 밴되었습니다. - by {inter.author.name}")
    else:
        await dm.send(f"밴되었습니다. - by {inter.author.name}")


cleanoption = md1.NewOptionList()
cleanoption.make_option(name="amount", description="채팅청소하는 수", required=False, type=Type.INTEGER)


@slash.command(name="clean", description="채팅청소하는 엄청난 명령어", options=cleanoption.options)
@slash_commands.has_guild_permissions(manage_messages=True)
@slash_commands.bot_has_guild_permissions(manage_messages=True)
async def _clean(inter: SlashInteraction):
    amount: int = inter.get('amount')
    channel1 = inter.channel
    await channel1.purge(limit=int(amount))
    await inter.reply(f"<@{inter.author.id}>님이 {str(amount)}만큼 채팅청소 했어요!")
    time.sleep(3)
    await inter.delete()


@slash.command(name="feedback", description="피드백을 줄 수 있는 명령어")
async def _feedback(inter: SlashInteraction):
    embed1 = discord.Embed(name="이 봇의 시스템 정보들", description="여러가지 링크들")
    embed1.set_author(name=inter.author.name, icon_url=inter.author.avatar_url)
    embed1.add_field(name="Github", value="[링크](https://github.com/MisileLab/furluck-bot)")
    await inter.reply(embed=embed1)


@slash.command(name="specialthanks", description="Thank you for helping me")
async def _specialthanks(inter: SlashInteraction):
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
    clicklistener: ClickListener = msg.create_click_listnener(timeout=30)

    # noinspection PyShadowingNames
    @clicklistener.not_from_user(inter.author, reset_timeout=False)
    async def wrong_user(inter: SlashInteraction):
        await inter.reply("You are not owner!", ephemeral=True)

    # noinspection PyShadowingNames
    @clicklistener.matching_id("buttonhelping")
    async def buttonhelping(inter: SlashInteraction):
        embed2 = discord.Embed(name="Helping hands", description="Thank you")
        embed2.add_field(name="EQUENOS", value="Make github pull requests, dislash.py developer")
        embed2.add_field(name="Rapptz", value="discord.py developer")
        embed2.add_field(name="Python Developers", value="Python is good ~~(Except Speed)~~")
        await inter.edit(embed=embed2, components=[])

    # noinspection PyShadowingNames
    @clicklistener.timeout
    async def timeout(inter: SlashInteraction):
        await inter.edit(embed=embed1, components=[])


muteoption = md1.NewOptionList()
muteoption.make_option(name="member", description="뮤트할 사람", required=True, type=Type.USER)
muteoption.make_option(name="reason", description="왜 뮤트함?", required=False, type=Type.STRING)


@slash.command(name="mute", description="상대방을 입막습니다! 읍읍", options=muteoption.options)
@slash_commands.has_guild_permissions(manage_messages=True)
@slash_commands.bot_has_guild_permissions(manage_messages=True)
async def _mute(inter: SlashInteraction):
    member: discord.Member = inter.get('member')
    reason = inter.get('reason', None)
    role1 = discord.utils.get(inter.guild.roles, name='뮤트')
    await md1.mute_command(role1, inter, member, reason)

unmuteoption = md1.NewOptionList()
unmuteoption.make_option(name="member", description="언뮤트할 사람", required=True, type=Type.USER)
unmuteoption.make_option(name="reason", description="왜 언뮤트함?", required=False, type=Type.STRING)


@slash.command(name="unmute", description="상대방을 입 막지 않습니다. 뮤트 멈춰!", options=unmuteoption.options)
@slash_commands.has_guild_permissions(manage_messages=True)
@slash_commands.bot_has_guild_permissions(manage_messages=True)
async def _unmute(inter: SlashInteraction):
    member: discord.Member = inter.get('member')
    reason = inter.get('reason', None)
    guild = inter.guild
    role1 = discord.utils.get(guild.roles, name='뮤트')
    await member.remove_roles(role1, reason=reason)
    if reason is None:
        await inter.reply(f"<@{inter.author.id}>님이 <@{member.id}>님을 언뮤트하였습니다!")
    else:
        await inter.reply(f"<@{inter.author.id}님이 {reason}이라는 이유로 <@{member.id}>님을 언뮤트하였습니다!")


calculateoption = md1.NewOptionList()
calculateoption.make_option(name="calculate", description="계산할 식", required=True, type=Type.STRING)


@slash.command(name="calculate", description="계산을 할 수 있는 명령어", options=calculateoption.options)
async def _calculate(inter: SlashInteraction):
    calculate = inter.get('calculate')
    try:
        result = simpleeval.simple_eval(calculate)
    except ValueError:
        await inter.reply(f"<@{inter.author.id}>님, 계산식이 틀린 것 같습니다")
    except ZeroDivisionError:
        await inter.reply("0으로 나누다?")
    else:
        await inter.reply(f"<@{inter.author.id}>님, 계산 결과가 {result}입니다.")


guckrioption = md1.NewOptionList()
guckrioption.make_option(name="member", description="격리할 사람", required=True, type=Type.USER)
guckrioption.make_option(name="reason", description="격리하는 이유", required=False, type=Type.STRING)


@slash.command(name="guckri", description="격리하는 명령어", guild_ids=icecreamhappydiscord, options=guckrioption.options)
@slash_commands.has_guild_permissions(administrator=True)
@slash_commands.bot_has_guild_permissions(administrator=True)
async def _guckri(inter: SlashInteraction):
    member = inter.get('member')
    reason = inter.get('reason', None)
    role1 = inter.guild.get_role(802733890221375498)
    await member.add_roles(role1, reason=reason)
    await inter.reply(content=md2.guckristring(reason, inter, member))


guckridisableoption = md1.NewOptionList()
guckridisableoption.make_option(name="member", description="격리 해제할 멤버", required=True, type=Type.USER)
guckridisableoption.make_option(name="reason", description="격리 해제하는 이유", required=False, type=Type.STRING)


@slash.command(name="notguckri", description="격리해제하는 명령어", guild_ids=icecreamhappydiscord,
               options=guckridisableoption.options)
@slash_commands.has_guild_permissions(administrator=True)
@slash_commands.bot_has_guild_permissions(administrator=True)
async def _guckridisable(inter: SlashInteraction):
    member = inter.get('member')
    reason = inter.get('reason', None)
    role1 = inter.guild.get_role(802733890221375498)
    await member.remove_roles(role1, reason=reason)
    await inter.reply(content=md2.notguckristring(reason, inter, member))


weatheroption = md1.NewOptionList()
weatheroption.make_option(name="position", description="날씨를 알고 싶은 장소", required=False, type=Type.STRING)


@slash.command(name="weather", description="날씨를 알려주는 명령어 (네이버 날씨)", options=weatheroption.options)
async def _weather(inter: SlashInteraction):
    await inter.reply(type=5)
    position = inter.get('position', None)
    try:
        weatherdata: md1.Weather = md1.WeatherBrowser(position).get_weather_data()
    except ValueError:
        await inter.edit(content="이름이 맞지 않는 것 같아요!")
    else:
        await inter.edit(content=None, embed=md2.set_weather_embed(weatherdata, position))


bitlyoption = md1.NewOptionList()
bitlyoption.make_option(name="url", description="길지 않게 만들 링크", required=True, type=Type.STRING)


@slash.command(name="bitly", description="링크를 길지 않게 만들어주는 명령어", options=bitlyoption.options)
async def _bitly(inter: SlashInteraction):
    longurl = inter.get('url')
    shorturl = md1.shortlink([longurl])
    shorturl2 = str(shorturl).replace("['", "").replace("']", "")
    await inter.reply(f"<@{inter.author.id}>님 링크가 {shorturl2} 로 변한것 같아요!")


randomoption = md1.NewOptionList()
randomoption.make_option(name="min", description="최소 숫자", required=True, type=Type.INTEGER)
randomoption.make_option(name="max", description="최대 숫자", required=True, type=Type.INTEGER)


@slash.command(name="random", description="랜덤으로 숫자를 굴려주는 명령어", options=randomoption.options)
async def _random(inter: SlashInteraction):
    x = inter.get('min')
    y = inter.get('max')
    await inter.reply(secrets.SystemRandom().randint(x, y))


getwarnoption = md1.NewOptionList()
getwarnoption.make_option(name="member", description="누구의 주의를 볼거임?", type=Type.USER, required=False)


@slash.command(name="getwarn", description="주의를 보는 세상 간단한 명령어", options=getwarnoption.options)
async def _getwarn(inter: SlashInteraction):
    member: discord.Member = inter.get('member', inter.author.id)
    warndata = md1.warn(memberid=member.id, amount=0, get=True)
    await inter.reply(f"{member.display_name}님의 주의 개수는 {warndata['warn']}개에요!")


warnoption = md1.NewOptionList()
warnoption.make_option(name="member", description="주의를 줄 사람", required=True, type=Type.USER)
warnoption.make_option(name="amount", description="주의를 얼마나 줄거임?", required=True, type=Type.INTEGER)
warnoption.make_option(name="reason", description="주의를 주는 이유", required=False, type=Type.STRING)


@slash_commands.has_guild_permissions(administrator=True)
@slash_commands.bot_has_guild_permissions(administrator=True)
@slash.command(name="warn", description="주의를 주는 세상 복잡한 명령어", options=warnoption.options)
async def _warn(inter: SlashInteraction):
    member = inter.get('member')
    reason = inter.get('reason', None)
    amount = inter.get('amount')
    warndata = md1.warn(memberid=member.id, amount=0, get=True)
    warndata = md1.warn(memberid=member.id, amount=warndata['warn'] + amount, get=False)
    message = md1.get_warn_message(reason, member.id, inter.author.id, warndata)
    await inter.reply(message)

unwarnoption = md1.NewOptionList()
unwarnoption.make_option(name="member", description="주의를 줄 사람", required=True, type=Type.USER)
unwarnoption.make_option(name="amount", description="주의를 얼마나 줄거임?", required=True, type=Type.INTEGER)
unwarnoption.make_option(name="reason", description="주의를 주는 이유", required=False, type=Type.STRING)


@slash_commands.has_guild_permissions(administrator=True)
@slash_commands.bot_has_guild_permissions(administrator=True)
@slash.command(name="unwarn", description="주의를 빼는 세상 이상한 명령어", options=unwarnoption.options)
async def _unwarn(inter: SlashInteraction):
    member = inter.get('member')
    reason = inter.get('reason', None)
    amount = inter.get('amount')
    warndata = md1.warn(memberid=member.id, amount=0, get=True)
    warndata = md1.warn(memberid=member.id, amount=warndata['warn'] - amount, get=False)
    message = md1.get_unwarn_message(reason, member.id, inter.author.id, warndata)
    await inter.reply(message)


hellochannel = md1.NewOptionList()
hellochannel.make_option(name="channel", description="인사 채널 (꼭 텍스트 채널이어야 함)", required=True, type=Type.CHANNEL)


@slash_commands.has_guild_permissions(administrator=True)
@slash_commands.bot_has_guild_permissions(administrator=True)
@slash.command(name="hellochannel", description="인사 채널을 설정하는 명령어", options=hellochannel.options)
async def _hellochannel(inter: SlashInteraction):
    channel = inter.get("channel")
    if type(channel) is discord.TextChannel:
        md1.serverdata("insaname", inter.author.guild.id, channel.id, False)
        await inter.reply(f"{channel.mention}으로 인사 채널이 변경되었어요!")


userchannel = md1.NewOptionList()
userchannel.make_option(name="user", description="호감도를 확인할 유저", required=False, type=Type.USER)


@slash.command(name="helpingme", description="제작자가 직접 주는 호감도 확인용", options=userchannel.options)
async def _helpinghands(inter: SlashInteraction):
    user = inter.get("user", inter.author)
    try:
        embedhelping = md2.set_helpingrank_embed(inter, user)
        if embedhelping is None:
            raise TypeError
    except md2.DataisNone():
        await inter.reply("그 플레이어의 데이터가 없는 것 같아요!")
    except TypeError:
        await inter.reply("플레이어의 데이터를 가져오는 과정으로 오류가 난 것 같아요!")
    else:
        await inter.reply(embed=embedhelping)


noticeother = md1.NewOptionList()
noticeother.make_option(name="description", description="설명", required=True, type=Type.STRING)


@slash.command(name="noticeother", description="공지를 하는 명령어", options=noticeother.options)
async def _notice(inter: SlashInteraction, description: str):
    md2.detect_admin(inter)
    await inter.reply(type=5)
    embednotice = discord.Embed(title="공지", description=description, color=0xed2f09)
    embednotice.set_footer(text="by MisileLab", icon_url=inter.author.avatar_url)
    getchannel = md1.noticeusingbot(inter.author.guild.id, 0, True)
    for i1 in getchannel:
        try:
            channel: discord.TextChannel = await Client.fetch_channel(i1["gongjiid"])
            await channel.send(embed=embednotice)
        except (AttributeError, discord.NotFound):
            pass
        else:
            await inter.edit(content="공지를 성공적으로 전달했어요!")


setnotice = md1.NewOptionList()
setnotice.make_option(name="channel", description="봇 공지 채널", required=True, type=Type.CHANNEL)


@slash_commands.has_guild_permissions(manage_messages=True, manage_channels=True)
@slash_commands.bot_has_guild_permissions(manage_messages=True, manage_channels=True)
@slash.command(name="setnotice", description="봇 공지 채널을 정하는 명령어", options=setnotice.options)
async def _setnotice(inter: SlashInteraction):
    channel = inter.get("setnotice")
    md1.noticeusingbot(inter.author.guild.id, channel.id, False)
    await inter.reply(f"{channel.mention}으로 공지 채널이 변경되었어요!")


@slash_commands.cooldown(10, 600)
@slash.command(name="mining", description="How to 얻는다, 600초 당 10번 씩 가능")
async def _mining(inter: SlashInteraction):
    md1.miningmoney(inter.author.id)
    random1 = secrets.SystemRandom().randint(1, 20)
    if random1 != 1:
        await inter.reply(f"<@{inter.author.id}>님에게 돈을 줬어요.")
    else:
        await inter.reply(f"<@{inter.author.id}>님에게 돈을 줬어요. ㅠㅠ")


@slash.command(name='getmoney', description='자신의 돈을 확인하는 명령어')
async def _getmoney(inter: SlashInteraction):
    getmoney = md1.getmoney(inter.author.id)
    await inter.reply(f"<@{inter.author.id}>님의 돈 : {getmoney}원")


dobak = md1.NewOptionList()
dobak.make_option(name="money", description="도박할 돈", required=True, type=Type.INTEGER)


@slash.command(name='dobak', description="도박하는 명령어, 확률은 50%, 메이플이 아님", options=dobak.options)
async def _dobak(inter: SlashInteraction, money: int):
    try:
        md1.dobakmoney(inter.author.id, money)
    except md1.FailedDobak:
        await inter.reply(f"<@{inter.author.id}>님이 도박에서 실패했어요. ㅠㅠ")
    except md1.DontHaveMoney:
        await inter.reply(f"<@{inter.author.id}>님의 돈이 부족해요!")
    else:
        await inter.reply(f"<@{inter.author.id}>님이 도박에 성공했어요!")


logoption = md1.NewOptionList()
logoption.make_option(name="channel", description="로그 채널", type=Type.CHANNEL, required=True)


@slash.command(name="log", description="로그 채널을 지정하는 재밌는 명령어", options=logoption.options)
async def _log(inter: SlashInteraction):
    channel = inter.get("channel")
    md1.serverdata('logid', inter.author.guild.id, channel.id, False)
    await inter.reply(f"로그 채널이 {channel.mention}으로 지정되었어요!")


serverinfo = md1.NewOptionList()
serverinfo.make_option(name="serverid", description="서버 ID", type=Type.STRING, required=False)


@slash.command(name="serverinfo", description="서버 정보를 알려주는 명령어", options=serverinfo.options)
async def _serverinfo(inter: SlashInteraction):
    await inter.reply("서버의 정보를 찾고 있어요!")
    guildid = inter.get("serverid", inter.author.guild.id)
    try:
        guild = await md1.get_guilds(guildid, Client, inter)
    except Exception as e:
        raise e
    else:
        embed1 = md1.make_guildinfo_embed(guild, inter)
        await inter.edit(embed=embed1, content=None)


userinfo = md1.NewOptionList()
userinfo.make_option(name="userid", description="유저 ID", type=Type.STRING, required=False)


@slash.command(name="userinfo", description="유저의 정보를 알려주는 명령어", options=userinfo.options)
async def _userinfo(inter: SlashInteraction):
    userid = inter.get("serverid", inter.author.id)
    await inter.reply("유저를 찾는 중이에요!")
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


createvoteoption = md1.NewOptionList()
createvoteoption.make_option(name="name", description="투표 이름", required=True, type=Type.STRING)
createvoteoption.make_option(name="description", description="설명", required=False, type=Type.STRING)
createvoteoption.make_option(name="timeout", description="투표 만료 단위 : 초", required=False, type=Type.INTEGER)


@slash.command(name="createvote", description="투표를 만드는 명령어", options=createvoteoption.options)
@commands.guild_only()
@commands.cooldown(10, 600)
async def _createvote(inter: SlashInteraction):
    await inter.reply(type=5)
    name = inter.get("name")
    description = inter.get("description", None)
    timeout = inter.get('timeout', '3600')
    embed = discord.Embed(title=name, description=description)
    component = md1.NewActionRow()
    component.add_button(style=ButtonStyle.green, name="O", custom_id="accept")
    component.add_button(style=ButtonStyle.red, name="X", custom_id="deny")
    votelol = md1.Vote()
    msg = await inter.edit(embed=embed, components=component.components)
    on_click: ClickListener = msg.create_click_listener(timeout=timeout)
    await md1.vote_listener(on_click, votelol, embed, inter)


# noinspection PyUnusedLocal
@slash.command(name="hypixel", description="하이픽셀 api를 사용하는 엄청난 명령어들", guild_ids=devserver)
@commands.guild_only()
async def _hypixel(inter):
    pass


playeroption = md1.NewOptionList()
playeroption.make_option(name="playername", description="플레이어의 이름", required=True, type=Type.STRING)


# noinspection PyBroadException
@_hypixel.sub_command(name="player", description="플레이어의 기본적인 스탯을 확인하는 명령어", options=playeroption.options,
                      guild_ids=devserver)
async def _player(inter: SlashInteraction):
    name = inter.get_option("player").options.get("playername").value
    try:
        responses: md1.Responses = await md1.except_error_information(inter=inter, name=name)
    except Exception as e:
        raise e
        
    else:
        response = next(responses.responses1)
        response2 = next(responses.responses1)
        if response is False or response2 is None:
            await inter.reply("서버 안에서 알 수 없는 에러가 났습니다.")
        else:
            embed = md1.create_player_embed(name, response, response2)
            await inter.reply(embed=embed)


@_hypixel.sub_command(name="rankhistory", description="플레이어의 랭크 기록을 확인하는 명령어", options=playeroption.options,
                      guild_ids=devserver)
async def _hypixelrankhistory(inter: SlashInteraction):
    await inter.reply(type=5)
    name = inter.get_option("rankhistory").options.get("playername").value
    try:
        response = await md1.except_error_history(inter, name)
    except Exception as e:
        await inter.edit("클라이언트 안에서 알 수 없는 에러가 났습니다.")
        raise e
    else:
        if response is False:
            await inter.edit("서버 안에서 알 수 없는 에러가 났습니다.")
        else:
            components = md1.rankhistorycomponents(response)
            msg = await inter.edit(content=f"{name}의 랭크 기록입니다.", components=[ActionRow(components)])
            inter = await msg.wait_for_dropdown()
            labels = [option.label for option in inter.select_menu.selected_options]
            embed = md1.rankhistoryembed(labels=labels, name=name, response=response)
            await msg.edit(content=None, embed=embed, components=[])

Client.run(token)
