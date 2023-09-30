from trevigiano.client import plugin

from .constants import periods

PLUGIN = plugin.Plugin()

COMMAND = PLUGIN.command
CONTEXT = PLUGIN.context


@COMMAND.command(
    PLUGIN,
    name="события",
    description="События",
    period=periods.PERIOD,
)
async def callback(context: "CONTEXT.Context") -> None:
    EMBED = context.embed

    await context.respond(
        embed=EMBED.embed(
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
