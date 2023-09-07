from bot.common import plugins

from ._periods import period

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts


@commands.command(
    plugin,
    name="события",
    description="События",
    period=period,
)
async def callback(context: contexts.Context) -> None:
    events = plugin.model.economics.events

    # fmt: off
    await context.respond(embed=context.embed(
        "default",
        description="\n".join([
            "\n".join([
                f"# {event.title}",
                f"> {event.description}",
            ])
            for event in events
        ]),
    ))
    # fmt: on
