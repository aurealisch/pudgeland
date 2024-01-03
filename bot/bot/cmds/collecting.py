from random import choice as random_choice

from crescent import Context as crescent_Context

from bot.modules.plugin import Plugin
from bot.utils import command
from bot.utils.decorate import decorate as d
from bot.utils.embed import embed
from bot.utils.emoji import Emoji
from bot.utils.humanize import humanize as h

plugin = Plugin()


@plugin.include
@command.command("сбор", description="Сбор")
class Command(command.Command):
    async def run(self, context: crescent_Context) -> None:
        database = plugin.model.database
        configuration = plugin.model.configuration

        id_ = str(context.user.id)

        user = await database.fetch_or_insert_user_by_id(id_)

        banana_quantity = sum(
            [
                random_choice(
                    range(
                        configuration["collecting_range_start"],
                        configuration["collecting_range_stop"],
                    )
                )
                for _ in range(user.monkey)
            ]
        )

        await database.increase_user_column_value_by_id(id_, "banana", banana_quantity)

        await context.respond(
            embeds=embed(
                "banana",
                title="collecting",
                description=f"+{d(h(banana_quantity))} {Emoji.banana} (Всего: {d(h(user.banana + banana_quantity))})",
            )
        )
