import string
import typing

import crescent

from bot.common import contexts, plugins
from bot.common.abc import commands
from bot.common.command import cooldowns

plugin = plugins.Plugin()

period = cooldowns.Period(seconds=2, milliseconds=500)  # 2.5 seconds


@typing.final
@plugin.include
@crescent.hook(cooldowns.cooldown(period=period))
@crescent.command(name="события", description="События")
class EventsCommand(commands.CommandABC):
    async def run(self, context: contexts.Context) -> None:
        await context.defer(True)

        description = string.whitespace

        events = plugin.model.economics.events

        for event in events:
            description += "\n".join([f"# {event.title}", f"> {event.description}"])

        await context.respond(
            ephemeral=True,
            embed=context.embed(
                "default",
                description=description,
            ),
        )
