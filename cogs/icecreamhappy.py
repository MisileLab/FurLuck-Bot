from discord.ext.commands import Cog
from dislash.interactions.slash_interaction import SlashInteraction
from dislash.slash_commands.slash_command import SlashCommand, Type
from dislash import slash_commands as slash
import modules.module2 as md2

icecreamhappydiscord = [635336036465246218]


class icecreamhappyistroll(Cog):
    def __init__(self, bot):
        self.Client = bot
    guckrioption = SlashCommand()
    guckrioption.add_option(name="member", description="격리할 사람", required=True, type=Type.USER)
    guckrioption.add_option(name="reason", description="격리하는 이유", required=False, type=Type.STRING)

    @slash.command(name="guckri", description="격리하는 명령어", guild_ids=icecreamhappydiscord, options=guckrioption.options)
    @slash.has_guild_permissions(administrator=True)
    @slash.bot_has_guild_permissions(administrator=True)
    async def _guckri(self, inter: SlashInteraction):
        member = inter.get('member')
        reason = inter.get('reason', None)
        role1 = inter.guild.get_role(802733890221375498)
        await member.add_roles(role1, reason=reason)
        await inter.reply(content=md2.guckristring(reason, inter, member))

    guckridisableoption = SlashCommand()
    guckridisableoption.add_option(name="member", description="격리 해제할 멤버", required=True, type=Type.USER)
    guckridisableoption.add_option(name="reason", description="격리 해제하는 이유", required=False, type=Type.STRING)

    @slash.command(name="notguckri", description="격리해제하는 명령어", guild_ids=icecreamhappydiscord,
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