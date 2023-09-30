from trevigiano.client import plugins

from .constants import (
    emojis,
    groups,
    periods,
)

PLUGIN = plugins.Plugin()

COMMANDS = PLUGIN.commands
CONTEXTS = PLUGIN.contexts


@COMMANDS.command(
    PLUGIN,
    name="репутация",
    description="Репутация",
    period=periods.PERIOD,
    group=groups.GROUP,
)
async def callback(context: "CONTEXTS.Context") -> None:
    EMBEDS = context.embeds
    HUMANIZES = context.humanizes

    USERS = await PLUGIN.model.database.leaders(
        PLUGIN.model.configuration.leaders.take,
        user_keys="reputation",
        sort_order=PLUGIN.model.configuration.leaders.sort.order,
    )

    EMBED = EMBEDS.embed("default")

    for INDEX, USER in enumerate(USERS):
        name = "\u0020"

        POSITION = INDEX + 1

        if POSITION in emojis.emoji:
            name += emojis.emoji[POSITION]

        name += f"#{POSITION}"

        EMBED.add_field(
            name=name,
            # fmt: off
            value="\n".join([
                f"<@{USER.partial.id}>",
                f"Репутация: `{HUMANIZES.humanize(USER.partial.reputation)}`",
            ])
            # fmt: on
        )

    await context.respond(embed=EMBED)


plugin = PLUGIN
