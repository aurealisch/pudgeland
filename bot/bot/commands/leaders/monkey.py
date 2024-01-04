from crescent import Context as crescent_Context

from bot.modules.plugin import Plugin
from bot.utilities import command
from bot.utilities.decorate import decorate
from bot.utilities.embed import embed
from bot.utilities.humanize import humanize

from ._groups import group

plugin = Plugin()

_ = lambda integer: decorate(humanize(integer))  # noqa: E731


@plugin.include
@command.command("обезьян", description="Лидеры обезьян", group=group)
class Command(command.Command):
    async def run(self, context: crescent_Context) -> None:
        emoji = plugin.model.emoji

        emojis = {
            1: emoji.leaders_first,
            2: emoji.leaders_second,
            3: emoji.leaders_third,
        }

        await context.respond(
            embeds=embed(
                "monkey",
                title="leaders-monkey",
                description="\n".join(
                    [
                        f"{emojis[position]} **#{position}** <@{user.id}> {_(user.monkey)}"
                        for position, user in enumerate(
                            await plugin.model.database.select_descending_users_by_column(
                                "monkey"
                            ),
                            start=1,
                        )
                    ]
                ),
            )
        )
