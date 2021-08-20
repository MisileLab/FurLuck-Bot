from discord.ext.commands import Cog
from dislash import SlashInteraction, Type, slash_command
from dislash import application_commands as slash
from .modules import module2 as md2
from .modules.module2 import NoneSlashCommand

icecreamhappydiscord = [635336036465246218]


class icecreamhappyistroll(Cog):
    def __init__(self, bot):
        self.Client = bot
    guckrioption = NoneSlashCommand()
    guckrioption.add_option(name="member", description="격리할 사람", required=True, type=Type.USER)
    guckrioption.add_option(name="reason", description="격리하는 이유", required=False, type=Type.STRING)

    @slash_command(name="guckri", description="격리하는 명령어", guild_ids=icecreamhappydiscord, options=guckrioption.options)
    @slash.has_guild_permissions(administrator=True)
    @slash.bot_has_guild_permissions(administrator=True)
    async def _guckri(self, inter: SlashInteraction):
        member = inter.get('member')
        reason = inter.get('reason', None)
        role1 = inter.guild.get_role(802733890221375498)
        await member.add_roles(role1, reason=reason)
        await inter.reply(content=md2.guckristring(reason, inter, member))

    guckridisableoption = NoneSlashCommand()
    guckridisableoption.add_option(name="member", description="격리 해제할 멤버", required=True, type=Type.USER)
    guckridisableoption.add_option(name="reason", description="격리 해제하는 이유", required=False, type=Type.STRING)

    @slash_command(name="notguckri", description="격리해제하는 명령어", guild_ids=icecreamhappydiscord,
                   options=guckridisableoption.options)
    @slash.has_guild_permissions(administrator=True)
    @slash.bot_has_guild_permissions(administrator=True)
    async def _guckridisable(self, inter: SlashInteraction):
        member = inter.get('member')
        reason = inter.get('reason', None)
        role1 = inter.guild.get_role(802733890221375498)
        await member.remove_roles(role1, reason=reason)
        await inter.reply(content=md2.notguckristring(reason, inter, member))


def setup(bot):
    bot.add_cog(icecreamhappyistroll(bot))
