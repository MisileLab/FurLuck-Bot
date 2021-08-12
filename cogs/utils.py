from discord.ext import commands
from dislash.interactions.message_components import ActionRow, Button, ButtonStyle
from .modules.module2 import NoneSlashCommand
from dislash import OptionType as Type
from dislash import slash_commands as slash
from dislash.interactions import SlashInteraction
from discord.ext.commands import Cog
from dislash.slash_commands.utils import ClickListener
import simpleeval
import cpuinfo
import discord
import time
from .modules import module1 as md1
from .modules import module2 as md2
import secrets


class utils(Cog):
    def __init__(self, bot):
        self.Client = bot

    @slash.command(name="bot", description="봇의 정보를 알려주는 명령어")
    async def _bot(self, inter: SlashInteraction):
        before = time.monotonic()
        await inter.reply(type=5)
        ping = time.monotonic() - before
        cpuinfo1 = cpuinfo.get_cpu_info()
        embed1 = md1.make_embed_bot_information(inter, cpuinfo1, ping, self.Client)
        await inter.edit(content=None, embed=embed1)

    @slash.command(name="feedback", description="피드백을 줄 수 있는 명령어")
    async def _feedback(self, inter: SlashInteraction):
        embed1 = discord.Embed(name="이 봇의 시스템 정보들", description="여러가지 링크들")
        embed1.set_author(name=inter.author.name, icon_url=inter.author.avatar_url)
        embed1.add_field(name="Github", value="[링크](https://github.com/MisileLab/furluck-bot)")
        await inter.reply(embed=embed1)

    @slash.command(name="specialthanks", description="Thank you for helping me")
    async def _specialthanks(self, inter: SlashInteraction):
        embed1 = discord.Embed(name="Helping hands", description="Thank you")
        embed1.set_author(name=inter.author.name, icon_url=inter.author.avatar_url)
        embed1.add_field(name="Misile#2134", value="Written by me")
        embed1.add_field(name="You", value="Using my bot")
        embed1.add_field(name="FurLuck", value="This bot image author")
        msg = await inter.reply(embed=embed1, components=[ActionRow(Button(style=ButtonStyle.green,
                                                                           label="Click Please",
                                                                           custom_id="buttonhelping"))])
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

    calculateoption = NoneSlashCommand()
    calculateoption.add_option(name="calculate", description="계산할 식", required=True, type=Type.STRING)

    @slash.command(name="calculate", description="계산을 할 수 있는 명령어", options=calculateoption.options)
    async def _calculate(self, inter: SlashInteraction):
        calculate = inter.get('calculate')
        try:
            result = simpleeval.simple_eval(calculate)
        except ValueError:
            await inter.reply(f"<@{inter.author.id}>님, 계산식이 틀린 것 같습니다")
        except ZeroDivisionError:
            await inter.reply("0으로 나누다?")
        else:
            await inter.reply(f"<@{inter.author.id}>님, 계산 결과가 {result}입니다.")

    weatheroption = NoneSlashCommand()
    weatheroption.add_option(name="position", description="날씨를 알고 싶은 장소", required=False, type=Type.STRING)

    @slash.command(name="weather", description="날씨를 알려주는 명령어 (네이버 날씨)", options=weatheroption.options)
    async def _weather(self, inter: SlashInteraction):
        await inter.reply(type=5)
        position = inter.get('position', None)
        try:
            weatherdata: md1.Weather = md1.WeatherBrowser(position).get_weather_data()
        except ValueError:
            await inter.edit(content="이름이 맞지 않는 것 같아요!")
        else:
            await inter.edit(content=None, embed=md2.set_weather_embed(weatherdata, position))

    bitlyoption = NoneSlashCommand()
    bitlyoption.add_option(name="url", description="길지 않게 만들 링크", required=True, type=Type.STRING)

    @slash.command(name="bitly", description="링크를 길지 않게 만들어주는 명령어", options=bitlyoption.options)
    async def _bitly(self, inter: SlashInteraction):
        longurl = inter.get('url')
        shorturl = md1.shortlink([longurl])
        shorturl2 = str(shorturl).replace("['", "").replace("']", "")
        await inter.reply(f"<@{inter.author.id}>님 링크가 {shorturl2} 로 변한것 같아요!")

    randomoption = NoneSlashCommand()
    randomoption.add_option(name="min", description="최소 숫자", required=True, type=Type.INTEGER)
    randomoption.add_option(name="max", description="최대 숫자", required=True, type=Type.INTEGER)

    @slash.command(name="random", description="랜덤으로 숫자를 굴려주는 명령어", options=randomoption.options)
    async def _random(self, inter: SlashInteraction):
        x = inter.get('min')
        y = inter.get('max')
        await inter.reply(secrets.SystemRandom().randint(x, y))

    userchannel = NoneSlashCommand()
    userchannel.add_option(name="user", description="호감도를 확인할 유저", required=False, type=Type.USER)

    @slash.command(name="helpingme", description="제작자가 직접 주는 호감도 확인용", options=userchannel.options)
    async def _helpinghands(self, inter: SlashInteraction):
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

    noticeother = NoneSlashCommand()
    noticeother.add_option(name="description", description="설명", required=True, type=Type.STRING)

    @slash.command(name="noticeother", description="공지를 하는 명령어", options=noticeother.options)
    async def _notice(self, inter: SlashInteraction, description: str):
        md2.detect_admin(inter)
        await inter.reply(type=5)
        embednotice = discord.Embed(title="공지", description=description, color=0xed2f09)
        embednotice.set_footer(text="by MisileLab", icon_url=inter.author.avatar_url)
        getchannel = md1.noticeusingbot(inter.author.guild.id, 0, True)
        for i1 in getchannel:
            try:
                channel: discord.TextChannel = await self.Client.fetch_channel(i1["gongjiid"])
                await channel.send(embed=embednotice)
            except (AttributeError, discord.NotFound):
                pass
            else:
                await inter.edit(content="공지를 성공적으로 전달했어요!")

    @slash.cooldown(10, 600)
    @slash.command(name="mining", description="How to 얻는다, 600초 당 10번 씩 가능")
    async def _mining(self, inter: SlashInteraction):
        md1.miningmoney(inter.author.id)
        random1 = secrets.SystemRandom().randint(1, 20)
        if random1 != 1:
            await inter.reply(f"<@{inter.author.id}>님에게 돈을 줬어요.")
        else:
            await inter.reply(f"<@{inter.author.id}>님에게 돈을 줬어요. ㅠㅠ")

    @slash.command(name='getmoney', description='자신의 돈을 확인하는 명령어')
    async def _getmoney(self, inter: SlashInteraction):
        getmoney = md1.getmoney(inter.author.id)
        await inter.reply(f"<@{inter.author.id}>님의 돈 : {getmoney}원")

    dobak = NoneSlashCommand()
    dobak.add_option(name="money", description="도박할 돈", required=True, type=Type.INTEGER)

    @slash.command(name='dobak', description="도박하는 명령어, 확률은 50%, 메이플이 아님", options=dobak.options)
    async def _dobak(self, inter: SlashInteraction, money: int):
        try:
            md1.dobakmoney(inter.author.id, money)
        except md1.FailedDobak:
            await inter.reply(f"<@{inter.author.id}>님이 도박에서 실패했어요. ㅠㅠ")
        except md1.DontHaveMoney:
            await inter.reply(f"<@{inter.author.id}>님의 돈이 부족해요!")
        else:
            await inter.reply(f"<@{inter.author.id}>님이 도박에 성공했어요!")

    logoption = NoneSlashCommand()
    logoption.add_option(name="channel", description="로그 채널", type=Type.CHANNEL, required=True)

    @slash.command(name="log", description="로그 채널을 지정하는 재밌는 명령어", options=logoption.options)
    async def _log(self, inter: SlashInteraction):
        channel = inter.get("channel")
        md1.serverdata('logid', inter.author.guild.id, channel.id, False)
        await inter.reply(f"로그 채널이 {channel.mention}으로 지정되었어요!")

    serverinfo = NoneSlashCommand()
    serverinfo.add_option(name="serverid", description="서버 ID", type=Type.STRING, required=False)

    @slash.command(name="serverinfo", description="서버 정보를 알려주는 명령어", options=serverinfo.options)
    async def _serverinfo(self, inter: SlashInteraction):
        await inter.reply("서버의 정보를 찾고 있어요!")
        guildid = inter.get("serverid", inter.author.guild.id)
        guild = await md1.get_guilds(guildid, self.Client, inter)
        embed1 = md1.make_guildinfo_embed(guild, inter)
        await inter.edit(embed=embed1, content=None)

    userinfo = NoneSlashCommand()
    userinfo.add_option(name="userid", description="유저 ID", type=Type.STRING, required=False)

    @slash.command(name="userinfo", description="유저의 정보를 알려주는 명령어", options=userinfo.options)
    async def _userinfo(self, inter: SlashInteraction):
        userid = inter.get("serverid", inter.author.id)
        await inter.reply("유저를 찾는 중이에요!")
        try:
            user1: discord.User = self.Client.get_user(int(userid))
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

    createvoteoption = NoneSlashCommand()
    createvoteoption.add_option(name="name", description="투표 이름", required=True, type=Type.STRING)
    createvoteoption.add_option(name="description", description="설명", required=False, type=Type.STRING)
    createvoteoption.add_option(name="timeout", description="투표 만료 단위 : 초", required=False, type=Type.INTEGER)

    @slash.command(name="createvote", description="투표를 만드는 명령어", options=createvoteoption.options)
    @commands.guild_only()
    @commands.cooldown(10, 600)
    async def _createvote(self, inter: SlashInteraction):
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


def setup(bot):
    bot.add_cog(utils(bot))
