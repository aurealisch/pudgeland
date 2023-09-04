import string

from bot.common import plugins

from ._periods import period

plugin = plugins.Plugin()


@plugin.include
@plugin.commands.command(
    "события",
    description="События",
    period=period,
)
async def callback(context: plugin.contexts.Context) -> None:
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
