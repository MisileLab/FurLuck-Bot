from discord.ext import commands
from dislash.interactions.message_components import ActionRow
from dislash.interactions.slash_interaction import SlashInteraction
from dislash import slash_commands as slash
from dislash import OptionType as Type
from .modules import module1 as md1
from discord.ext.commands import Cog
from .modules.module2 import NoneSlashCommand

playeroption = NoneSlashCommand()
playeroption.add_option(name="playername", description="플레이어의 이름", required=True, type=Type.STRING)


class hypixel(Cog):
    def __init__(self, bot):
        self.Client = bot

    # noinspection PyUnusedLocal
    @slash.command(name="hypixel", description="하이픽셀 api를 사용하는 엄청난 명령어들")
    @commands.guild_only()
    async def _hypixel(self, inter: SlashInteraction):
        pass

    # noinspection PyBroadException
    @_hypixel.sub_command(name="player", description="플레이어의 기본적인 스탯을 확인하는 명령어", options=playeroption.options)
    async def _player(self, inter: SlashInteraction):
        name = inter.get_option("player").get("playername").value
        responses: md1.Responses = await md1.except_error_information(inter=inter, name=name)
        response = next(responses.responses1)
        response2 = next(responses.responses1)
        if response is False or response2 is None:
            await inter.reply("서버 안에서 알 수 없는 에러가 났습니다.")
        else:
            embed = md1.create_player_embed(name, response, response2)
            await inter.reply(embed=embed)

    @_hypixel.sub_command(name="rankhistory", description="플레이어의 랭크 기록을 확인하는 명령어", options=playeroption.options)
    async def _hypixelrankhistory(self, inter: SlashInteraction):
        # sourcery no-metrics
        await inter.reply(type=5)
        name = inter.get_option("rankhistory").get("playername").value
        try:
            response = await md1.except_error_history(inter, name)
        except Exception as e:
            await inter.edit("클라이언트 안에서 알 수 없는 에러가 났습니다.")
            raise e
        else:
            if response is False:
                await inter.edit("서버 안에서 알 수 없는 에러가 났습니다.")
            else:
                components = md1.rankhistorycomponents(response)
                msg = await inter.edit(content=f"{name}의 랭크 기록입니다.", components=[ActionRow(components)])
                inter = await msg.wait_for_dropdown()
                labels = [option.label for option in inter.select_menu.selected_options]
                embed = md1.rankhistoryembed(labels=labels, name=name, response=response)
                await msg.edit(content=None, embed=embed, components=[])


def setup(bot):
    bot.add_cog(hypixel(bot))
