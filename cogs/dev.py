from random import SystemRandom
import hashlib
import discord
from dislash.application_commands.utils import ClickListener
from dislash.interactions.message_components import ActionRow, Button, ButtonStyle
from dislash.interactions.slash_interaction import SlashInteraction
from discord.ext.commands.cog import Cog
from dislash import slash_commands


devserver = [812339145942237204, 635336036465246218, 863950154055155712]


class dev(Cog):
    def __init__(self, bot):
        self.Client = bot

    @slash_commands.command(name="ticket", guild_ids=devserver)
    async def _ticket(self):
        pass

    @slash_commands.command(name="create", description="티켓을 만드는 명령어", guild_ids=devserver)
    @slash_commands.bot_has_guild_permissions(manage_channels=True)
    async def _createticket(self, inter: SlashInteraction):
        components = [ActionRow(Button(style=ButtonStyle.gray, label="티켓 만들기", custom_id="createticket"))]
        msg = await inter.reply(content="티켓을 만들려면 버튼을 눌러주세요!", components=components)
        clicklistener: ClickListener = msg.create_click_listener()

        @clicklistener.matching_id("createticket")
        async def createticketlol(inter: SlashInteraction):
            guild: discord.Guild = inter.guild
            ticketowner: discord.Member = guild.get_member(inter.author.id)
            overwrites = {
                guild.deafult_role: discord.PermissionOverwrite(view_channels=False),
                ticketowner: discord.PermissionOverwrite(view_channels=True)
            }
            randomlol = str(hashlib.sha512(str(SystemRandom().randint(1, 1000000000)).encode('utf-8')).hexdigest())
            list1 = [randomlol[SystemRandom().randint(0, 512)] for _ in range(1, 6)]
            str1 = list1[0:6]
            channel: discord.TextChannel = await guild.create_text_channel(f'ticket-{str1}', overwrites=overwrites)
            components = [ActionRow(Button(style=ButtonStyle.red, label="채널 없애기", custom_id="deleteticket"))]
            msg = await channel.send(f'티켓이 만들어졌습니다! <@{inter.author.id}>', components=components)
            clicklistener2: ClickListener = msg.create_click_listener()

            @clicklistener2.matching_id("deleteticket")
            async def deleteticket(inter: SlashInteraction):
                channel.delete()


def setup(bot):
    bot.add_cog(dev(bot))