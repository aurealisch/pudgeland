from trevigiano.client import plugins

from .common import periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts


@commands.command(
    plugin,
    name="события",
    description="События",
    period=periods.period,
)
async def callback(context: "contexts.Context") -> None:
    events = plugin.model.database.events

    embeds = context.embeds

    embed = embeds.embed

    await context.respond(
        embed=embed(
            "default",
            description="\n".join(
                [
                    "\n".join(
                        [
                            f"# {event.title}",
                            f"> {event.description}",
                        ]
                    )
                    for event in events
                ]
            ),
        )
    )
