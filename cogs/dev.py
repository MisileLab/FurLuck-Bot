from dislash.application_commands.utils import ClickListener
from dislash.interactions.message_components import ActionRow, Button, ButtonStyle
from dislash.interactions.slash_interaction import SlashInteraction
from discord.ext.commands.cog import Cog
from dislash import slash_commands
from .modules import module2 as md2


devserver = [812339145942237204, 635336036465246218, 863950154055155712]


class dev(Cog):
    def __init__(self, bot):
        self.Client = bot

    @slash_commands.command(name="ticket", guild_ids=devserver)
    async def _ticket(self, inter: SlashInteraction):
        pass

    @_ticket.sub_command(name="create", description="티켓을 만드는 명령어", guild_ids=devserver)
    @slash_commands.bot_has_guild_permissions(manage_channels=True)
    @slash_commands.has_guild_permissions(manage_channels=True)
    async def _createticket(self, inter: SlashInteraction):
        components = [ActionRow(Button(style=ButtonStyle.gray, label="티켓 만들기", custom_id="createticket"))]
        msg = await inter.reply(content="티켓을 만들려면 버튼을 눌러주세요!", components=components)
        clicklistener: ClickListener = msg.create_click_listener()
        await md2.createticketlistener(clicklistener, inter)


def setup(bot):
    bot.add_cog(dev(bot))
