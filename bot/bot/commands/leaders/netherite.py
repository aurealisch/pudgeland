from crescent import Context as crescent_Context

from bot.modules.plugin import Plugin
from bot.utilities import command
from bot.utilities.decorate import decorate as d
from bot.utilities.embed import embed
from bot.utilities.emoji import Emoji
from bot.utilities.humanize import humanize as h

from .constants.groups import group

plugin = Plugin()


@plugin.include
@command.command("незерита", description="Лидеры незерита", group=group)
class Command(command.Command):
    async def run(self, context: crescent_Context) -> None:
        emojis = {
            1: Emoji.leaders_first,
            2: Emoji.leaders_second,
            3: Emoji.leaders_third,
        }

        await context.respond(
            embeds=embed(
                "netherite",
                title="leaders-netherite",
                description="\n".join(
                    [
                        f"{emojis[position]} **#{position}** <@{user.id}> {d(h(user.netherite))}"
                        for position, user in enumerate(
                            await plugin.model.database.select_descending_users_by_column(
                                "netherite"
                            ),
                            start=1,
                        )
                    ]
                ),
            )
        )
