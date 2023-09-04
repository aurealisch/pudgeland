import string

from bot.common import plugins
from bot.common.command import commands, contexts, cooldowns

plugin = plugins.Plugin()


@plugin.include
@commands.command(
    "события",
    description="События",
    period=cooldowns.Period(
        seconds=2,
        milliseconds=500,
    ),  # 2.5 seconds
)
async def callback(context: contexts.Context) -> None:
    await context.defer(True)

    description = string.whitespace

    events = plugin.model.economics.events

    for event in events:
        description += "\n".join(
            [
                f"# {event.title}",
                f"> {event.description}",
            ],
        )

    await context.respond(
        ephemeral=True,
        embed=context.embed(
            "default",
            description=description,
        ),
    )
