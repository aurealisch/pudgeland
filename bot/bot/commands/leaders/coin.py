from crescent import Context as crescent_Context

from bot.modules.plugin import Plugin
from bot.utilities import command
from bot.utilities.decorate import decorate as d
from bot.utilities.embed import embed
from bot.utilities.emoji import Emoji
from bot.utilities.humanize import humanize as h

from ._groups import group

plugin = Plugin()


@plugin.include
@command.command("монет", description="Лидеры монет", group=group)
class Command(command.Command):
    async def run(self, context: crescent_Context) -> None:
        emojis = {
            1: Emoji.leaders_first,
            2: Emoji.leaders_second,
            3: Emoji.leaders_third,
        }

        await context.respond(
            embeds=embed(
                "coin",
                title="leaders-coin",
                description="\n".join(
                    [
                        f"{emojis[position]} **#{position}** <@{user.id}> {d(h(user.coin))}"
                        for position, user in enumerate(
                            await plugin.model.database.select_descending_users_by_column(
                                "coin"
                            ),
                            start=1,
                        )
                    ]
                ),
            )
        )
