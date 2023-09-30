from trevigiano.client import plugins

from .constants import periods

PLUGIN = plugins.Plugin()

COMMANDS = PLUGIN.commands
CONTEXTS = PLUGIN.contexts


@COMMANDS.command(
    PLUGIN,
    name="события",
    description="События",
    period=periods.PERIOD,
)
async def callback(context: "CONTEXTS.Context") -> None:
    EMBEDS = context.embeds

    await context.respond(
        embed=EMBEDS.embed(
            "default",
            # fmt: off
            description="\n".join([
                "\n".join([
                    f"# {EVENT.title}",
                    f"> {EVENT.description}",
                ])
                for EVENT in PLUGIN.model.database.events
            ])
            # fmt: on
        )
    )


plugin = PLUGIN
