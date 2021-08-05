from dislash.interactions.slash_interaction import SlashInteraction
import module1 as md1
import discord

def make_embed(member: discord.Member):
    embed = discord.Embed(title="멤버 입장", description=f'{member.name}님이 {member.guild.name}에 입장했어요!', color=0x00a352)
    embed.add_field(name='현재 인원', value=str(len([m for m in member.guild.members if not m.bot])) + '명')
    embed.set_footer(text=md1.todaycalculate())
    embed.set_thumbnail(url=member.avatar_url)
    return embed

class notadmin(Exception):
    def __init__(self, message:discord.Message=None):
        self.message = message

def detect_admin(inter: SlashInteraction, message: discord.Message=None):
    if inter.author.id != 338902243476635650:
        raise notadmin(message)
    return True

class DataisNone(Exception):
    pass

def set_helpingrank_embed(inter:SlashInteraction, user:discord.Member):
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

def set_weather_embed(weatherdata, position:str):
    embed1 = discord.Embed(name="현재 날씨", description=f"{position}의 날씨에요!")
    embed1.set_thumbnail(url=weatherdata.weatherimage)
    embed1.add_field(name="현재 온도", value=weatherdata.temp)
    embed1.add_field(name="최고 온도", value=weatherdata.maxtemp)
    embed1.add_field(name="최저 온도", value=weatherdata.mintemp)
    embed1.add_field(name="체감 온도", value=weatherdata.sensibletemp)
    embed1.add_field(name="날씨 상황", value=weatherdata.cast)
    embed1.add_field(name="미세먼지 농도(μg/m3)", value=weatherdata.dust)
    embed1.add_field(name="미세먼지 위험 단계", value=weatherdata.dust_txt)
    embed1.add_field(name="초미세먼지 농도(μg/m3)", value=weatherdata.ultra_dust)
    embed1.add_field(name="초미세먼지 위험 단계", value=weatherdata.ultra_dust_txt)
    embed1.add_field(name="오존 농도(ppm)", value=weatherdata.ozone)
    embed1.add_field(name="오존 위험 단계", value=weatherdata.ozonetext)
    return embed1