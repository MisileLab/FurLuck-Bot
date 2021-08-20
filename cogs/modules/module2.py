from __future__ import annotations
import hashlib
from random import SystemRandom
from dislash.application_commands.utils import ClickListener
from dislash.interactions.application_command import SlashCommand
from dislash.interactions.message_components import ActionRow, Button, ButtonStyle
from dislash.interactions.slash_interaction import SlashInteraction
import psutil
import discord
from dislash import application_command as application_commands
from . import module1 as md1


def get_true_member(member: discord.Member):
    return str(len([m for m in member.guild.members if not m.bot]))


def make_member_join_embed(member: discord.Member):
    embed = discord.Embed(title="멤버 입장",
                          description=f'{member.name}님이 {member.guild.name}에 입장했어요!',
                          color=0x00a352)
    embed.add_field(name='현재 인원', value=get_true_member(member) + '명')
    embed.set_footer(text=md1.todaycalculate())
    embed.set_thumbnail(url=member.avatar_url)
    return embed


class notadmin(Exception):
    def __init__(self, message: discord.Message = None):
        self.message = message


def detect_admin(inter: SlashInteraction, message: discord.Message = None):
    if inter.author.id != 338902243476635650:
        raise notadmin(message)
    return True


class DataisNone(Exception):
    pass


def set_helpingrank_embed(inter: SlashInteraction, user: discord.Member):
    helpingyouandme = md1.helpingyou(user.id)["helpingme"]
    if helpingyouandme is None:
        raise DataisNone
    helpingrank = md1.get_helping_rank(helpingyouandme, user.id)
    if helpingrank is None:
        return None
    embedhelping = discord.Embed(title="호감도 현황", description=f"{user.name}님! 고마워요!")
    embedhelping.set_author(name="Misile#2134", url="https://github.com/MisileLab",
                            icon_url="https://i.imgur.com/6y4X4aw.png")
    embedhelping.add_field(name="호감도 칭호", value=helpingrank)
    return embedhelping


def set_weather_embed(weatherdata: md1.Weather, position: str):
    embed1 = set_weather_embed_temp(weatherdata, position)
    embed1.add_field(name="날씨 상황", value=weatherdata.cast)
    embed1.add_field(name="미세먼지 농도(μg/m3)", value=weatherdata.dust)
    embed1.add_field(name="미세먼지 위험 단계", value=weatherdata.dust_txt)
    embed1.add_field(name="초미세먼지 농도(μg/m3)", value=weatherdata.ultra_dust)
    embed1.add_field(name="초미세먼지 위험 단계", value=weatherdata.ultra_dust_txt)
    embed1.add_field(name="오존 농도(ppm)", value=weatherdata.ozone)
    embed1.add_field(name="오존 위험 단계", value=weatherdata.ozonetext)
    return embed1


def set_weather_embed_temp(weatherdata: md1.Weather, position: str):
    embed1 = discord.Embed(name="현재 날씨", description=f"{position}의 날씨에요!")
    embed1.set_thumbnail(url=weatherdata.weatherimage)
    embed1.add_field(name="현재 온도", value=weatherdata.temp)
    embed1.add_field(name="최고 온도", value=weatherdata.maxtemp)
    embed1.add_field(name="최저 온도", value=weatherdata.mintemp)
    embed1.add_field(name="체감 온도", value=weatherdata.sensibletemp)
    return embed1


class sub_error_handler:
    def __init__(self, error, inter: SlashInteraction):
        self.error = error
        self.inter = inter

    @staticmethod
    async def missingpermissionerrorhandling(missing_perms, inter: SlashInteraction):
        await inter.reply(f"권한이 부족해요! 부족한 권한 : {missing_perms}")

    async def errorhandling(self):
        if isinstance(self.error, application_commands.MissingPermissions):
            await self.missingpermissionerrorhandling(self.error.missing_perms, self.inter)

        elif isinstance(self.error, application_commands.BotMissingPermissions):
            await self.inter.reply(f"봇의 권한이 부족해요! 부족한 권한 : {self.error.missing_perms}")

        elif isinstance(self.error, application_commands.CommandOnCooldown):
            await self.inter.reply(f"이 명령어는 {self.error.retry_after}초 뒤에 사용할 수 있어요!")

        elif isinstance(self.error, notadmin):
            await self.messageerrorhandlinglol()

    async def messageerrorhandlinglol(self):
        if self.error.message is None:
            await self.inter.reply("이 명령어는 당신이 쓸 수 없어요!")
        else:
            await self.error.message.edit("이 명령어는 당신이 쓸 수 없어요!")


def cpuandram(inter: SlashInteraction, cpuinfo1):
    embed1 = discord.Embed(title="봇 정보", description="펄럭 봇의 엄청난 봇 정보")
    embed1.set_author(name=inter.author.name, icon_url=inter.author.avatar_url)
    embed1.add_field(name="CPU 이름", value=cpuinfo1["brand_raw"])
    embed1.add_field(name="CPU Hz", value=cpuinfo1["hz_actual_friendly"])
    embed1.add_field(name="램 전체 용량", value=str(
        round(psutil.virtual_memory().total / (1024 * 1024 * 1024))) + "GB")
    embed1.add_field(name="램 사용 용량", value=str(
        round(psutil.virtual_memory().used / (1024 * 1024 * 1024))) + "GB")
    embed1.add_field(name="램 용량 퍼센테이지(%)", value=str(
        psutil.virtual_memory().percent))
    return embed1


def guckristring(reason: str or None, inter: SlashInteraction, member: discord.Member):
    if reason is None:
        return f"<@{inter.author.id}>님이 <@{member.id}>님을 격리하였습니다!"
    return f"<@{inter.author.id}님이 {reason}이라는 이유로 <@{member.id}님을 격리하였습니다!"


def notguckristring(reason: str or None, inter: SlashInteraction, member: discord.Member):
    if reason is None:
        return (f"<@{inter.author.id}>님이 <@{member.id}>님을 격리해제 하였습니다!")
    return (f"<@{inter.author.id}님이 {reason}이라는 이유로 <@{member.id}님을 격리해제 하였습니다!")


def make_member_remove_embed(member: discord.Member):
    embed = discord.Embed(title="멤버 퇴장", description=f'{member.name}님이 {member.guild.name}에서 퇴장했어요. ㅠㅠ', color=0xff4747)
    embed.add_field(name='현재 인원', value=str(len([m for m in member.guild.members if not m.bot])) + '명')
    embed.set_footer(text=md1.todaycalculate())
    embed.set_thumbnail(url=member.avatar_url)
    return embed


def NoneSlashCommand():
    return SlashCommand('none', 'none')


async def specialthankslistener(clicklistener: ClickListener, inter: SlashInteraction, embed1: discord.Embed):
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


async def createticketlistener(clicklistener: ClickListener, inter: SlashInteraction):
    @clicklistener.matching_id("createticket")
    async def createticketlol(inter: SlashInteraction):
        channel: discord.Channel = await createticketchannel(inter)
        components = [ActionRow(Button(style=ButtonStyle.red, label="채널 없애기", custom_id="deleteticket"))]
        msg = await channel.send(f'티켓이 만들어졌습니다! <@{inter.author.id}>', components=components)
        clicklistener2: ClickListener = msg.create_click_listener()

        @clicklistener2.matching_id("deleteticket")
        async def deleteticket(inter: SlashInteraction):
            await channel.delete()


async def createticketchannel(inter: SlashInteraction):
    ticketowner: discord.Member = inter.author.guild.get_member(inter.author.id)
    overwrites = {
        inter.author.guild.default_role: discord.PermissionOverwrite(view_channel=False),
        ticketowner: discord.PermissionOverwrite(view_channel=True)
    }
    randomlol = str(hashlib.sha512(str(SystemRandom().randint(1, 1000000000)).encode('utf-8')).hexdigest())
    list1 = [randomlol[SystemRandom().randint(0, 128)] for _ in range(6)]
    str1 = ''.join(list1)
    return await inter.author.guild.create_text_channel(f'ticket-{str1}', overwrites=overwrites)


def get_unmute_string(reason: str or None, inter: SlashInteraction, member: discord.Member):
    if reason is None:
        return f"<@{inter.author.id}>님이 <@{member.id}>님을 언뮤트하였습니다!"
    return f"<@{inter.author.id}>님이 {reason}이라는 이유로 <@{member.id}>님을 언뮤트하였습니다!"


def make_userinfo_embed(user1: discord.Member, inter: SlashInteraction):
    embed1 = discord.Embed(name="유저의 정보", description=f"{user1.name}의 정보에요!")
    embed1.set_thumbnail(url=user1.avatar_url)
    embed1.set_author(name=inter.author.name, icon_url=inter.author.avatar_url)
    embed1.set_footer(text=md1.todaycalculate())
    embed1.add_field(name="봇 여부", value=str(user1.bot))
    embed1.add_field(name="시스템 계정 여부", value=str(user1.system))
    embed1.add_field(name="계정이 생성된 날짜", value=str(md1.makeformat(user1.created_at)))
    return embed1
