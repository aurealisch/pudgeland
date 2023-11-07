import datetime
import random

import crescent

from trevigiano import plugins

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts

period = datetime.timedelta(hours=1, minutes=30)

group = crescent.Group("сбор", description="Сбор")


@plugin.include
@commands.command("бананов",
                  description="Сбор бананов",
                  period=period,
                  group=group)
class Command(commands.Command):

    async def call(self, context: contexts.Context) -> None:
        """Description"""
        database = plugin.model.database

        emoji = context.emoji
        humanize = context.humanize

        identifier = str(context.user.id)

        user = await database.upsert(identifier)

        range_ = plugin.model.configuration.get("plugins").get("collect").get(
            "range")

        foxQuantity = user.fox

        berryQuantity = sum([
            random.choice(range(range_.get("start"), range_.get("stop")))
            for _ in range(foxQuantity)
        ])

        title = f"{emoji.Emoji.banana} Сбор бананов"
        description = f"```+{humanize.humanize(berryQuantity)} бананов (Всего: {user.berry + berryQuantity})```"  # noqa: E501

        await database.increment(identifier, "berry", berryQuantity)

        await context.respond(embed=context.embed.embed(
            "bananas", title=title, description=description))
