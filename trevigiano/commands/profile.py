import datetime

from trevigiano import plugins

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts

period = datetime.timedelta(seconds=2, milliseconds=500)


@plugin.include
@commands.command("профиль", description="Профиль", period=period)
class Command(commands.Command):

    async def call(self, context: contexts.Context) -> None:
        """Description"""
        decorate = context.decorate
        emoji = context.emoji
        humanize = context.humanize

        user = await plugin.model.database.upsert(str(context.user.id))

        berry = user.berry
        fox = user.fox

        coin = user.coin

        netheriteScrap = user.netheriteScrap
        diamond = user.diamond

        title = f"{emoji.Emoji.profile} Профиль"
        # fmt: off
        description = "\n".join([
            f"{emoji.Emoji.berry} Ягоды: {decorate.decorate(humanize.humanize(berry))}" if berry != 0 else '\u0020',
            f"{emoji.Emoji.fox} Лисы: {decorate.decorate(humanize.humanize(fox))}" if fox != 0 else '\u0020',

            f"{emoji.Emoji.coin} Монеты: {decorate.decorate(humanize.humanize(coin))}" if coin != 0 else '\u0020',

            f"{emoji.Emoji.netherite.scrap} Незеритовые ломы: {decorate.decorate(humanize.humanize(netheriteScrap))}" if netheriteScrap != 0 else '\u0020',
            f"{emoji.Emoji.diamond} Алмазы: {decorate.decorate(humanize.humanize(diamond))}" if diamond != 0 else '\u0020',
        ])
        # fmt: on

        await context.respond(embed=context.embed.embed(
            "profile", title=title, description=description))
