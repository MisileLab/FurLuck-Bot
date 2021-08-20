import discord
from dislash import application_commands, slash_command
from dislash import OptionType, SlashInteraction
from discord.ext.commands.cog import Cog
from .modules import module2 as md2
from .modules import module1 as md1


devserver = [812339145942237204, 635336036465246218, 863950154055155712]


class dev(Cog):
    def __init__(self, bot):
        self.Client = bot

    @slash_command(name="recaptcha")
    async def _recaptcha(self, inter: SlashInteraction):
        pass  # cause subcommand

    @_recaptcha.sub_command(name="off", guild_ids=devserver, description="auth 기능을 끄는 명령어")
    @application_commands.has_guild_permissions(administrator=True)
    @application_commands.bot_has_guild_permissions(administrator=True)
    async def _offrecaptcha(self, inter: SlashInteraction):
        md1.serverdata('recaptcha', inter.author.guild.id, 0, False)
        await inter.reply("완료되었습니다!")

    recaptchaonoption = md2.NoneSlashCommand()
    recaptchaonoption.add_option(name="role", description="성공할 시 줄 역할", type=OptionType.ROLE, required=True)

    @_recaptcha.sub_command(name="on", guild_ids=devserver, description="auth 기능을 키는 명령어",
                            options=recaptchaonoption.options)
    @application_commands.has_guild_permissions(administrator=True)
    @application_commands.bot_has_guild_permissions(administrator=True)
    async def _onrecaptcha(self, inter: SlashInteraction):
        role: discord.Role = inter.get_option("on").get("role")
        md1.serverdata('recaptcha', inter.author.guild.id, role.id, False)
        await inter.reply("완료되었습니다!")


def setup(bot):
    bot.add_cog(dev(bot))
