import crescent

from bot import plugins

from ..constants import groups, periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts

subGroup = crescent.SubGroup("незеритовых", groups.group, "Незеритовых")


@plugin.include
@commands.command(
    "ломов",
    description="Лидеры незеритовых ломов",
    period=periods.period,
    group=groups.group,
    subGroup=subGroup,
)
class Command(commands.Command):

    async def call(self, context: contexts.Context) -> None:
        """Description"""
        emoji = context.emoji

        users = await plugin.model.database.selectLeaders("netheriteScrap")

        emojis = {
            1: emoji.Emoji.first,
            2: emoji.Emoji.second,
            3: emoji.Emoji.third
        }

        title = f"{emoji.Emoji.netherite.scrap} Лидеры незеритовых ломов"

        description = "\n".join([
            f"{emojis[position]} **#{position}** <@{user.id}> {context.decorate.decorate(context.humanize.humanize(user.netheriteScrap))}"
            for position, user in enumerate(users, start=1)
        ])

        await context.respond(embed=context.embed.embed(
            "netheriteScraps", title=title, description=description))
