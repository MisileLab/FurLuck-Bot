from __future__ import annotations
from dislash.interactions.application_command import SlashCommand
from dislash.interactions.slash_interaction import SlashInteraction
import psutil
import discord
from dislash import application_command as slash_commands
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import module1 as md1


def get_true_member(member: discord.Member):
    return str(len([m for m in member.guild.members if not m.bot]))


def make_embed(member: discord.Member):
    embed = discord.Embed(title="멤버 입장", description=f'{member.name}님이 {member.guild.name}에 입장했어요!', color=0x00a352)
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
    async def MissingPermissonHandling(missing_perms, inter: SlashInteraction):
        await inter.reply(f"권한이 부족해요! 부족한 권한 : {missing_perms}")

    async def ErrorHandling(self):
        error = self.error
        inter = self.inter
        if isinstance(error, slash_commands.MissingPermissions):
            await self.MissingPermissonHandling(error.missing_perms, inter)

        elif isinstance(error, slash_commands.BotMissingPermissions):
            await inter.reply(f"봇의 권한이 부족해요! 부족한 권한 : {error.missing_perms}")

        elif isinstance(error, slash_commands.CommandOnCooldown):
            await inter.reply(f"이 명령어는 {error.retry_after}초 뒤에 사용할 수 있어요!")

        elif isinstance(error, notadmin):
            if error.message is None:
                await inter.reply("이 명령어는 당신이 쓸 수 없어요!")
            else:
                await error.message.edit("이 명령어는 당신이 쓸 수 없어요!")


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

