from dislash import slash_command, Type, SlashInteraction
from dislash import application_commands as slash
from discord.ext import commands
import discord
import time
from .modules import module1 as md1
from .modules.module2 import NoneSlashCommand
from .modules import module2 as md2


class admin(commands.Cog):
    def __init__(self, bot):
        self.Client = bot

    kickoption = NoneSlashCommand()
    kickoption.add_option(name="member", description="킥할 사람", required=True, type=Type.USER)
    kickoption.add_option(name="reason", description="왜 킥함?", required=False, type=Type.STRING)

    @slash_command(name="kick", description="상대를 서버 밖으로 날리는 명령어", options=kickoption.options)
    @slash.has_guild_permissions(kick_members=True)
    @slash.bot_has_guild_permissions(kick_members=True)
    async def _kick(self, inter: SlashInteraction):
        kickmember = inter.get('member')
        reason = inter.get('reason', None)
        await kickmember.kick(reason=reason)
        await inter.reply(f"<@{inter.author.id}>님으로 인하여 <@{kickmember.id}>가 킥 당했습니다.")

    banoption = NoneSlashCommand()
    banoption.add_option(name="member", description="밴할 멤버", required=True, type=Type.USER)
    banoption.add_option(name="reason", description="왜 밴함", required=False, type=Type.STRING)

    @slash_command(name="ban", description="상대를 서버 밖으로 영원히 날리는 명령어", options=banoption.options)
    @slash.has_guild_permissions(ban_members=True)
    @slash.bot_has_guild_permissions(ban_members=True)
    async def _ban(self, inter: SlashInteraction):
        banmember: discord.Member = inter.get('member')
        reason = inter.get('reason', None)
        await banmember.ban()
        await inter.reply(f"<@{inter.author.id}>님으로 인하여 <@{banmember.id}>가 밴되었습니다.")
        dm = await banmember.create_dm()
        if reason is not None:
            await dm.send(f"{reason}으로 인해 밴되었습니다. - by {inter.author.name}")
        else:
            await dm.send(f"밴되었습니다. - by {inter.author.name}")

    cleanoption = NoneSlashCommand()
    cleanoption.add_option(name="amount", description="채팅청소하는 수", required=False, type=Type.INTEGER)

    @slash_command(name="clean", description="채팅청소하는 엄청난 명령어", options=cleanoption.options)
    @slash.has_guild_permissions(manage_messages=True)
    @slash.bot_has_guild_permissions(manage_messages=True)
    async def _clean(self, inter: SlashInteraction):
        amount: int = inter.get('amount')
        channel1 = inter.channel
        await channel1.purge(limit=int(amount))
        await inter.reply(f'<@{inter.author.id}>님이 {amount}만큼 채팅청소 했어요!')
        time.sleep(3)
        await inter.delete()

    muteoption = NoneSlashCommand()
    muteoption.add_option(name="member", description="뮤트할 사람", required=True, type=Type.USER)
    muteoption.add_option(name="reason", description="왜 뮤트함?", required=False, type=Type.STRING)

    @slash_command(name="mute", description="상대방을 입막습니다! 읍읍", options=muteoption.options)
    @slash.has_guild_permissions(manage_messages=True)
    @slash.bot_has_guild_permissions(manage_messages=True)
    async def _mute(self, inter: SlashInteraction):
        member: discord.Member = inter.get('member')
        reason = inter.get('reason', None)
        role1 = discord.utils.get(inter.guild.roles, name='뮤트')
        await md1.mute_command(role1, inter, member, reason)

    unmuteoption = NoneSlashCommand()
    unmuteoption.add_option(name="member", description="언뮤트할 사람", required=True, type=Type.USER)
    unmuteoption.add_option(name="reason", description="왜 언뮤트함?", required=False, type=Type.STRING)

    @slash_command(name="unmute", description="상대방을 입 막지 않습니다. 뮤트 멈춰!", options=unmuteoption.options)
    @slash.has_guild_permissions(manage_messages=True)
    @slash.bot_has_guild_permissions(manage_messages=True)
    async def _unmute(self, inter: SlashInteraction):
        member: discord.Member = inter.get('member')
        reason = inter.get('reason', None)
        guild = inter.guild
        role1 = discord.utils.get(guild.roles, name='뮤트')
        await member.remove_roles(role1, reason=reason)
        await inter.reply(md2.get_unmute_string(reason, inter, member))

    getwarnoption = NoneSlashCommand()
    getwarnoption.add_option(name="member", description="누구의 주의를 볼거임?", type=Type.USER, required=False)

    @slash_command(name="getwarn", description="주의를 보는 세상 간단한 명령어", options=getwarnoption.options)
    async def _getwarn(self, inter: SlashInteraction):
        member: discord.Member = inter.get('member', inter.author.id)
        warndata = md1.warn(memberid=member.id, amount=0, get=True)
        await inter.reply(f"{member.display_name}님의 주의 개수는 {warndata['warn']}개에요!")

    warnoption = NoneSlashCommand()
    warnoption.add_option(name="member", description="주의를 줄 사람", required=True, type=Type.USER)
    warnoption.add_option(name="amount", description="주의를 얼마나 줄거임?", required=True, type=Type.INTEGER)
    warnoption.add_option(name="reason", description="주의를 주는 이유", required=False, type=Type.STRING)

    @slash.has_guild_permissions(administrator=True)
    @slash.bot_has_guild_permissions(administrator=True)
    @slash_command(name="warn", description="주의를 주는 세상 복잡한 명령어", options=warnoption.options)
    async def _warn(self, inter: SlashInteraction):
        member = inter.get('member')
        reason = inter.get('reason', None)
        amount = inter.get('amount')
        warndata = md1.warn(memberid=member.id, amount=0, get=True)
        warndata = md1.warn(memberid=member.id, amount=warndata['warn'] + amount, get=False)
        message = md1.get_warn_message(reason, member.id, inter.author.id, warndata)
        await inter.reply(message)

    unwarnoption = NoneSlashCommand()
    unwarnoption.add_option(name="member", description="주의를 줄 사람", required=True, type=Type.USER)
    unwarnoption.add_option(name="amount", description="주의를 얼마나 줄거임?", required=True, type=Type.INTEGER)
    unwarnoption.add_option(name="reason", description="주의를 주는 이유", required=False, type=Type.STRING)

    @slash.has_guild_permissions(administrator=True)
    @slash.bot_has_guild_permissions(administrator=True)
    @slash_command(name="unwarn", description="주의를 빼는 세상 이상한 명령어", options=unwarnoption.options)
    async def _unwarn(self, inter: SlashInteraction):
        member = inter.get('member')
        reason = inter.get('reason', None)
        amount = inter.get('amount')
        warndata = md1.warn(memberid=member.id, amount=0, get=True)
        warndata = md1.warn(memberid=member.id, amount=warndata['warn'] - amount, get=False)
        message = md1.get_unwarn_message(reason, member.id, inter.author.id, warndata)
        await inter.reply(message)

    hellochannel = NoneSlashCommand()
    hellochannel.add_option(name="channel", description="인사 채널 (꼭 텍스트 채널이어야 함)", required=True, type=Type.CHANNEL)

    @slash.has_guild_permissions(administrator=True)
    @slash.bot_has_guild_permissions(administrator=True)
    @slash_command(name="hellochannel", description="인사 채널을 설정하는 명령어", options=hellochannel.options)
    async def _hellochannel(self, inter: SlashInteraction):
        channel = inter.get("channel")
        if isinstance(channel, discord.TextChannel):
            md1.serverdata("insaname", inter.author.guild.id, channel.id, False)
            await inter.reply(f"{channel.mention}으로 인사 채널이 변경되었어요!")

    setnotice = NoneSlashCommand()
    setnotice.add_option(name="channel", description="봇 공지 채널", required=True, type=Type.CHANNEL)

    @slash.has_guild_permissions(manage_messages=True, manage_channels=True)
    @slash.bot_has_guild_permissions(manage_messages=True, manage_channels=True)
    @slash_command(name="setnotice", description="봇 공지 채널을 정하는 명령어", options=setnotice.options)
    async def _setnotice(self, inter: SlashInteraction):
        channel = inter.get("setnotice")
        md1.noticeusingbot(inter.author.guild.id, channel.id, False)
        await inter.reply(f"{channel.mention}으로 공지 채널이 변경되었어요!")


def setup(bot):
    bot.add_cog(admin(bot))
