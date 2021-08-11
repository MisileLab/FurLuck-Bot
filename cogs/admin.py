import modules.module1 as md1
from dislash import Type

kickoption = md1.NewOptionList()
kickoption.make_option(name="member", description="킥할 사람", required=True, type=Type.USER)
kickoption.make_option(name="reason", description="왜 킥함?", required=False, type=Type.STRING)


@slash.command(name="kick", description="상대를 서버 밖으로 날리는 명령어", options=kickoption.options)
@slash_commands.has_guild_permissions(kick_members=True)
@slash_commands.bot_has_guild_permissions(kick_members=True)
async def _kick(inter: SlashInteraction):
    kickmember = inter.get('member')
    reason = inter.get('reason', None)
    await kickmember.kick(reason=reason)
    await inter.reply(f"<@{inter.author.id}>님으로 인하여 <@{kickmember.id}>가 킥 당했습니다.")


banoption = md1.NewOptionList()
banoption.make_option(name="member", description="밴할 멤버", required=True, type=Type.USER)
banoption.make_option(name="reason", description="왜 밴함", required=False, type=Type.STRING)


@slash.command(name="ban", description="상대를 서버 밖으로 영원히 날리는 명령어", options=banoption.options)
@slash_commands.has_guild_permissions(ban_members=True)
@slash_commands.bot_has_guild_permissions(ban_members=True)
async def _ban(inter: SlashInteraction):
    banmember: discord.Member = inter.get('member')
    reason = inter.get('reason', None)
    await banmember.ban()
    await inter.reply(f"<@{inter.author.id}>님으로 인하여 <@{banmember.id}>가 밴되었습니다.")
    dm = await banmember.create_dm()
    if reason is not None:
        await dm.send(f"{reason}으로 인해 밴되었습니다. - by {inter.author.name}")
    else:
        await dm.send(f"밴되었습니다. - by {inter.author.name}")


cleanoption = md1.NewOptionList()
cleanoption.make_option(name="amount", description="채팅청소하는 수", required=False, type=Type.INTEGER)


@slash.command(name="clean", description="채팅청소하는 엄청난 명령어", options=cleanoption.options)
@slash_commands.has_guild_permissions(manage_messages=True)
@slash_commands.bot_has_guild_permissions(manage_messages=True)
async def _clean(inter: SlashInteraction):
    amount: int = inter.get('amount')
    channel1 = inter.channel
    await channel1.purge(limit=int(amount))
    await inter.reply(f'<@{inter.author.id}>님이 {amount}만큼 채팅청소 했어요!')
    time.sleep(3)
    await inter.delete()
